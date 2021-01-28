import csv
import subprocess
import time


import numpy as np


CONTAINER_IDS = ['96ed8d37252b', '9f16c2ad98bd']
GPU_IDX2CONTAINER_ID = {0: '96ed8d37252b', 1: '9f16c2ad98bd'}


def get_average_hr(container_id):
    output = subprocess.check_output(f'docker logs {container_id} | grep Total | tail -3', shell=True)
    hrs = []
    for line in output.decode('utf-8').splitlines():
        hrs.append(float(line.split()[5]))
    return np.mean(hrs)

def get_average_power_draw(gpu_idx):
    draws = []
    for i in range(10):
        output = subprocess.check_output(f'nvidia-smi -i {gpu_idx} --format=csv --query-gpu=power.draw', shell=True)
        draws.append(float(output.decode('utf-8').split()[2]))
        time.sleep(0.2)
    return np.mean(draws)


def set_params(gpu_idx, pl, clock_offset, mem_offset):
    subprocess.check_call(f'nvidia-smi -i {gpu_idx} -pl {pl}', shell=True)
    subprocess.check_call(f"nvidia-settings -a '[gpu:{gpu_idx}]/GPUGraphicsClockOffset[4]={clock_offset}'", shell=True)
    subprocess.check_call(f"nvidia-settings -a '[gpu:{gpu_idx}]/GPUMemoryTransferRateOffset[4]={mem_offset}'", shell=True)


if __name__ == '__main__':
    with open('eggs.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter='\t')
        for pl in range(350, 260, -10):
            for clock_offset in range(-500, 100, 50):
                for mem_offset in range(-200, 1500, 100):
                    for gpu_idx in sorted(GPU_IDX2CONTAINER_ID):
                        set_params(gpu_idx, pl, clock_offset, mem_offset)
                    time.sleep(65)
                    for gpu_idx in sorted(GPU_IDX2CONTAINER_ID):
                        power_draw = get_average_power_draw(gpu_idx)
                        hr = get_average_hr(GPU_IDX2CONTAINER_ID[gpu_idx])
                        csv_writer.writerow([gpu_idx, pl, clock_offset, mem_offset, hr, power_draw, hr/power_draw])
                        csvfile.flush()
