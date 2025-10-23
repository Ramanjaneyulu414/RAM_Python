We calculate the sum of absolute differences between consecutive elements.
That represents the minimum total number of operations needed.

Algorithm:
1. Read N and array A.
2. Initialize ans = 0.
3. For i = 1 to N-1:
   ans += abs(A[i] - A[i-1])
4. Print ans.