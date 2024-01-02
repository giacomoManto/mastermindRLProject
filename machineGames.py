from mastermind import board
import solver
from tqdm import tqdm
import multiprocessing as mp


def run_test():
    m = board()
    s = solver.mini_max()

    for a in range(1, 13):
        guess = s.makeGuess()
        response = m.makeGuess(guess)
        s.adjustMoves(guess, response)  
        if response[0] == 4:
            return a

if __name__ == '__main__':
    count = 10000
    async_results = []

    pool = mp.Pool(processes=10)
    jobs = []
    for unused in range(count):
        jobs.append(pool.apply_async(func=run_test))
    pool.close()
    result_list_tqdm = []
    for job in tqdm(jobs):
        result_list_tqdm.append(job.get())

    results = result_list_tqdm

    print(sum(results) / len(results))
    print(max(results))
    print(min(results))