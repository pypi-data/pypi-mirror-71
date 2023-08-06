#pragma once

#include "gs_def.h"
#include "cusha256.h"
#include "cudagol.h"

namespace apg {

    void GpuSearcher::pump(std::string seed, uint64_t epoch, std::vector<uint64_t> &vec) {

        int minibatch = this->num_universes;
        int maxgen = 21000;

        hash_container *hc = (hash_container*) this->xhc;
        uint4 *multiverse = (uint4*) this->xmc;

        cudaSetDevice(this->device);

        hc->create_hashes(seed, epoch);

        for (int sb = 0; sb < 1000000; sb += minibatch) {

            uint32_t* hi = hc->interesting + sb;
            uint32_t* hh = hc->d_B + sb * 8;

            exhaustFirstTile<<<(minibatch >> 2), 128>>>(hh, hi, multiverse);
            exhaustMultipleTiles<20, 20,  64><<<minibatch, 128>>>(2,  hi, hc->topology, multiverse, maxgen);
            exhaustMultipleTiles<38, 38, 128><<<minibatch, 256>>>(20, hi, hc->topology, multiverse, maxgen);
            exhaustMultipleTilesUltimate<92, 128, 128><<<minibatch, 512>>>(38, hi, hc->topology, multiverse, maxgen);
        }

        auto oldsize = vec.size();
        hc->extract_gems(epoch, 1000000, vec);
        std::cout << "Interesting universes: " << (vec.size() - oldsize) << " out of 1000000" << std::endl;

        // for (auto&& it : vec) { std::cout << it << ", "; }
        // std::cout << std::endl;

        cudaError_t err = cudaGetLastError();
        if (err != cudaSuccess) { std::cerr << "Error: " << cudaGetErrorString(err) << std::endl; }
    }

    GpuSearcher::GpuSearcher(int dev, int num_universes, std::string symmetry) {

        size_t free_mem = 0;
        size_t total_mem = 0;

        cudaMemGetInfo(&free_mem, &total_mem);

        std::cerr << "Memory statistics: " << free_mem << " free; " << total_mem << " total." << std::endl;

        int minibatch = 0;

        if        (free_mem < 2000000000ull) {
            minibatch = 10000;
        } else if (free_mem < 4000000000ull) {
            minibatch = 20000;
        } else if (free_mem < 8000000000ull) {
            minibatch = 50000;
        } else if (free_mem < 16000000000ull) {
            minibatch = 100000;
        } else {
            minibatch = 200000;
        }

        std::cerr << "Minibatch size: \033[32;1m " << minibatch << " \033[0m" << std::endl;

        this->num_universes = minibatch;
        this->symstring = symmetry;
        this->device = dev;
        auto hc = new hash_container();

        cudaMalloc((void**) &(this->xmc), ((uint64_t) minibatch) * 65536);

        this->xhc = (void*) hc;

        cudaSetDevice(dev);

        hc->spin_up(true, num_universes);
    }

    GpuSearcher::~GpuSearcher() {
        hash_container *hc = (hash_container*) this->xhc;

        cudaSetDevice(this->device);

        hc->tear_down();
        cudaFree(this->xmc);

        delete hc;
    }

}
