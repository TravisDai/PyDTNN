#!/bin/bash

export OMP_NUM_THREADS=2
mpirun -np 12 \
   python3 -u benchmarks_CNN.py \
         --model=simplecnn \
         --dataset=mnist \
         --dataset_train_path=../datasets/mnist \
         --dataset_test_path=../datasets/mnist \
         --batch_size=64 \
         --validation_split=0.2 \
         --num_epochs=10 \
         --optimizer=Adam \
         --learning_rate=0.001 \
         --loss_func=categorical_accuracy,categorical_cross_entropy \
         --parallel=data \
         --blocking_mpi \
         --dtype=float32 --evaluate
         #--test_as_validation
         # --profile
         #--enable_gpu

         #--evaluate \
         # 
         # --decay_rate=0.99 \
         # --epsilon=1e-08 \
         # --momentum=0.9 \ 
         # --steps_per_epoch=0 \
         # --evaluate=True \
         # --tracing=False \
         # --profile=False \
