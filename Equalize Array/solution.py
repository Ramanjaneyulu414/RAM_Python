# solution.py
import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    arr = [int(next(it)) for _ in range(n)]
    if n <= 1:
        print(0)
        return
    ans = 0
    for i in range(1, n):
        ans += abs(arr[i] - arr[i-1])
    print(ans)

if __name__ == "__main__":
    solve()