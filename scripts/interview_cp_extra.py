#!/usr/bin/env python3
"""Extra coding interview Q&As from 2025–2026 FAANG frequency research."""
from __future__ import annotations

from interview_helpers import (
    bullets,
    callout,
    code_block,
    figure_diagram,
    qa_block,
    steps,
)


def cp_extra_questions(start: int = 11) -> list[str]:
    """High-frequency problems not in the original top-10 lab set."""
    q: list[str] = []
    n = start

    q.append(
        qa_block(
            qnum=n,
            title="Best Time to Buy and Sell Stock",
            asked="Every FAANG — LC 121; top-5 frequency in 2025–2026 reports",
            difficulty="Easy",
            pattern="One pass · track min price",
            prompt=(
                "prices[i] is the stock price on day i. Choose one day to buy and a later day "
                "to sell to maximize profit. Return the max profit (0 if no profit)."
            ),
            sections=[
                (
                    "Clarify",
                    bullets(
                        [
                            "One transaction only (buy once, sell once).",
                            "Must sell after buy.",
                            "Empty / length-1 → 0.",
                        ]
                    ),
                ),
                (
                    "Diagram",
                    figure_diagram("stock-profit", "Track running minimum price"),
                ),
                (
                    "Step-by-step",
                    steps(
                        [
                            "Brute: try every buy/sell pair O(n²) — reject it.",
                            "Keep min_price seen so far while scanning left→right.",
                            "At each price, candidate = price − min_price; track best.",
                            "Time O(n), space O(1).",
                        ]
                    ),
                ),
                (
                    "Python",
                    code_block(
                        "python",
                        """def max_profit(prices):
    min_price, best = float("inf"), 0
    for p in prices:
        min_price = min(min_price, p)
        best = max(best, p - min_price)
    return best""",
                    ),
                ),
                (
                    "Follow-ups",
                    bullets(
                        [
                            "LC 122 unlimited transactions → sum all uphill segments.",
                            "LC 123 at most 2 → DP states.",
                            "Cooldown with cooldown → state machine DP (Amazon favorite).",
                        ]
                    ),
                ),
            ],
        )
    )
    n += 1

    q.append(
        qa_block(
            qnum=n,
            title="Minimum Window Substring",
            asked="Meta, Amazon, LinkedIn — LC 76; #4 in many 2026 frequency lists",
            difficulty="Hard",
            pattern="Sliding window · need/have counts",
            prompt=(
                "Given strings s and t, return the smallest substring of s that covers every "
                "character in t (including duplicates). Return \"\" if impossible."
            ),
            sections=[
                (
                    "Step-by-step",
                    steps(
                        [
                            "Build need counts for t; need_unique = number of distinct chars.",
                            "Expand right; update have counts; when a char's have hits need, "
                            "increment formed.",
                            "While formed == need_unique, shrink left; record best window.",
                            "Time O(|s| + |t|), space O(alphabet).",
                        ]
                    ),
                ),
                (
                    "Diagram",
                    figure_diagram("min-window", "Shrink while window still covers t"),
                ),
                (
                    "Python",
                    code_block(
                        "python",
                        """from collections import Counter

def min_window(s, t):
    need = Counter(t)
    missing = len(need)
    have = {}
    best_len, best = float("inf"), ""
    left = 0
    for right, ch in enumerate(s):
        have[ch] = have.get(ch, 0) + 1
        if ch in need and have[ch] == need[ch]:
            missing -= 1
        while missing == 0:
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best = s[left : right + 1]
            left_ch = s[left]
            have[left_ch] -= 1
            if left_ch in need and have[left_ch] < need[left_ch]:
                missing += 1
            left += 1
    return best""",
                    ),
                ),
                (
                    "Trap",
                    callout(
                        "Meta tip",
                        "<p>Practice explaining the formed/missing counter — interviewers stop "
                        "you if you nest O(|t|) scans inside the while loop.</p>",
                    ),
                ),
            ],
        )
    )
    n += 1

    q.append(
        qa_block(
            qnum=n,
            title="Maximum Subarray (Kadane)",
            asked="Amazon, Google, Microsoft — LC 53; Amazon OA staple",
            difficulty="Medium",
            pattern="Kadane · running best ending here",
            prompt=(
                "Find the contiguous subarray with the largest sum and return that sum."
            ),
            sections=[
                (
                    "Step-by-step",
                    steps(
                        [
                            "At each index: either extend previous run or start fresh at nums[i].",
                            "best_ending = max(nums[i], best_ending + nums[i]).",
                            "Track global max. Handles all-negative by picking the largest element.",
                            "Time O(n), space O(1).",
                        ]
                    ),
                ),
                (
                    "Diagram",
                    figure_diagram("kadane", "Kadane running sum"),
                ),
                (
                    "Python",
                    code_block(
                        "python",
                        """def max_sub_array(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best""",
                    ),
                ),
                (
                    "Follow-ups",
                    bullets(
                        [
                            "Return the actual subarray indices.",
                            "Circular maximum subarray.",
                            "2D Kadane (maximal rectangle sum) — Google follow-up.",
                        ]
                    ),
                ),
            ],
        )
    )
    n += 1

    q.append(
        qa_block(
            qnum=n,
            title="Search in Rotated Sorted Array",
            asked="Meta, Amazon, LinkedIn, Microsoft — LC 33",
            difficulty="Medium",
            pattern="Binary search · identify sorted half",
            prompt=(
                "nums was sorted ascending then rotated at an unknown pivot. Search for target "
                "in O(log n). Distinct values."
            ),
            sections=[
                (
                    "Step-by-step",
                    steps(
                        [
                            "Standard binary search frame. Mid always sits in a half that is sorted.",
                            "If nums[lo] ≤ nums[mid]: left half sorted. If target in [lo, mid), "
                            "search left; else right.",
                            "Else right half sorted — symmetric check.",
                            "Draw an example like [4,5,6,7,0,1,2] every time.",
                        ]
                    ),
                ),
                (
                    "Diagram",
                    figure_diagram("rotated-search", "Binary search on rotated array"),
                ),
                (
                    "Python",
                    code_block(
                        "python",
                        """def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1""",
                    ),
                ),
            ],
        )
    )
    n += 1

    q.append(
        qa_block(
            qnum=n,
            title="Top K Frequent Elements",
            asked="Amazon, Google, Meta, Microsoft — LC 347; universal heap question",
            difficulty="Medium",
            pattern="Hash map + heap / bucket sort",
            prompt=(
                "Given an integer array, return the k most frequent elements. Order of the "
                "answer does not matter."
            ),
            sections=[
                (
                    "Step-by-step",
                    steps(
                        [
                            "Count frequencies in a map O(n).",
                            "Option A: min-heap of size k → O(n log k).",
                            "Option B (often preferred): bucket sort by frequency → O(n).",
                            "Say both; implement one cleanly.",
                        ]
                    ),
                ),
                (
                    "Diagram",
                    figure_diagram("top-k-buckets", "Bucket sort by frequency"),
                ),
                (
                    "Python (bucket)",
                    code_block(
                        "python",
                        """from collections import Counter

def top_k_frequent(nums, k):
    freq = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for val, c in freq.items():
        buckets[c].append(val)
    out = []
    for c in range(len(buckets) - 1, 0, -1):
        for val in buckets[c]:
            out.append(val)
            if len(out) == k:
                return out
    return out""",
                    ),
                ),
            ],
        )
    )
    n += 1

    q.append(
        qa_block(
            qnum=n,
            title="Meeting Rooms II",
            asked="Meta (Facebook), Amazon, Bloomberg — premium classic",
            difficulty="Medium",
            pattern="Min-heap of end times / sweep line",
            prompt=(
                "Given meeting time intervals [start, end), find the minimum number of conference "
                "rooms required."
            ),
            sections=[
                (
                    "Step-by-step",
                    steps(
                        [
                            "Sort meetings by start time.",
                            "Min-heap stores end times of rooms in use.",
                            "If next start ≥ earliest end, reuse (pop); else allocate (push).",
                            "Answer = max heap size during the scan (or final size if you track peak).",
                        ]
                    ),
                ),
                (
                    "Diagram",
                    figure_diagram("meeting-rooms", "Heap of meeting end times"),
                ),
                (
                    "Python",
                    code_block(
                        "python",
                        """import heapq

def min_meeting_rooms(intervals):
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[0])
    heap = []  # end times
    for start, end in intervals:
        if heap and start >= heap[0]:
            heapq.heappop(heap)
        heapq.heappush(heap, end)
    return len(heap)""",
                    ),
                ),
                (
                    "Related",
                    "<p>Merge Intervals / Insert Interval / Non-overlapping — same family. "
                    "Sweep line with +1 at start and −1 at end also works.</p>",
                ),
            ],
        )
    )
    n += 1

    q.append(
        qa_block(
            qnum=n,
            title="Valid Parentheses",
            asked="Amazon, Google, Meta, Bloomberg — LC 20; common warmup / phone screen",
            difficulty="Easy",
            pattern="Stack",
            prompt=(
                "Given a string containing just '()[]{}', determine if the input string is valid: "
                "open brackets closed by the same type in the correct order."
            ),
            sections=[
                (
                    "Step-by-step",
                    steps(
                        [
                            "Scan left→right. Push opening brackets.",
                            "On closing: stack must be non-empty and top must match.",
                            "End with empty stack.",
                            "Time O(n), space O(n).",
                        ]
                    ),
                ),
                (
                    "Python",
                    code_block(
                        "python",
                        """def is_valid(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in pairs.values():
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
        else:
            return False
    return not stack""",
                    ),
                ),
                (
                    "Follow-ups",
                    bullets(
                        [
                            "Longest valid parentheses (Hard).",
                            "Minimum remove to make valid (Meta).",
                            "Generate parentheses (backtracking).",
                        ]
                    ),
                ),
            ],
        )
    )
    n += 1

    q.append(
        qa_block(
            qnum=n,
            title="Rotting Oranges",
            asked="Amazon, Microsoft, Google — LC 994; multi-source BFS favorite",
            difficulty="Medium",
            pattern="Multi-source BFS on grid",
            prompt=(
                "Grid of 0 (empty), 1 (fresh), 2 (rotten). Each minute, any fresh orange "
                "4-adjacent to a rotten one becomes rotten. Return minutes until all fresh are "
                "rotten, or -1 if impossible."
            ),
            sections=[
                (
                    "Step-by-step",
                    steps(
                        [
                            "Enqueue <em>all</em> initially rotten cells (multi-source BFS).",
                            "Count fresh oranges.",
                            "BFS level-by-level; each level = 1 minute; rot neighbors.",
                            "If fresh remains → -1; else minutes (careful: last wave may add a minute — "
                            "track correctly).",
                        ]
                    ),
                ),
                (
                    "Diagram",
                    figure_diagram("rotting-oranges", "Multi-source BFS rotting"),
                ),
                (
                    "Python",
                    code_block(
                        "python",
                        """from collections import deque

def oranges_rotting(grid):
    rows, cols = len(grid), len(grid[0])
    q, fresh = deque(), 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while q and fresh:
        for _ in range(len(q)):
            r, c = q.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    q.append((nr, nc))
        minutes += 1
    return minutes if fresh == 0 else -1""",
                    ),
                ),
            ],
        )
    )
    n += 1

    q.append(
        qa_block(
            qnum=n,
            title="Alien Dictionary",
            asked="Meta, Google — LC 269; hard topo-sort phone-screen closer",
            difficulty="Hard",
            pattern="Graph · topological sort from sorted words",
            prompt=(
                "You are given a list of words sorted lexicographically in an alien language. "
                "Derive any valid order of unique letters. Return \"\" if invalid."
            ),
            sections=[
                (
                    "Step-by-step",
                    steps(
                        [
                            "Compare consecutive words; first differing chars give an edge "
                            "earlier→later.",
                            "Invalid if word A is prefix of longer preceding word (\"abc\" before \"ab\").",
                            "Build graph + indegrees; Kahn BFS for a valid order.",
                            "If cycle / not all letters processed → \"\".",
                        ]
                    ),
                ),
                (
                    "Python sketch",
                    code_block(
                        "python",
                        """from collections import defaultdict, deque

def alien_order(words):
    graph = defaultdict(set)
    indeg = {c: 0 for w in words for c in w}
    for w1, w2 in zip(words, words[1:]):
        if w1.startswith(w2) and w1 != w2 and len(w1) > len(w2):
            return ""
        for a, b in zip(w1, w2):
            if a != b:
                if b not in graph[a]:
                    graph[a].add(b)
                    indeg[b] += 1
                break
    q = deque([c for c, d in indeg.items() if d == 0])
    order = []
    while q:
        c = q.popleft()
        order.append(c)
        for nxt in graph[c]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)
    return "".join(order) if len(order) == len(indeg) else "" """,
                    ),
                ),
            ],
        )
    )
    n += 1

    q.append(
        qa_block(
            qnum=n,
            title="Kth Largest Element in an Array",
            asked="Amazon, Meta, Google, Microsoft — LC 215",
            difficulty="Medium",
            pattern="Min-heap of size k / Quickselect",
            prompt=(
                "Find the kth largest element in an unsorted array. Note it is the kth largest "
                "in sorted order, not the kth distinct."
            ),
            sections=[
                (
                    "Step-by-step",
                    steps(
                        [
                            "Min-heap of size k: push all; pop when size > k; peek is answer O(n log k).",
                            "Quickselect (Hoare): average O(n) — mention for strong signal.",
                            "Sorting is O(n log n) — acceptable start, then optimize.",
                        ]
                    ),
                ),
                (
                    "Python (heap)",
                    code_block(
                        "python",
                        """import heapq

def find_kth_largest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]""",
                    ),
                ),
                (
                    "Related Amazon ask",
                    "<p>K Closest Points to Origin (LC 973) — same heap pattern with distance.</p>",
                ),
            ],
        )
    )

    return q
