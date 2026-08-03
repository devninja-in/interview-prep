#!/usr/bin/env python3
"""Competitive programming interview Q&As — research-backed FAANG favorites."""
from __future__ import annotations

from interview_helpers import code_block, drill_section, qa_block


def cp_questions() -> list[str]:
    q: list[str] = []

    q.append(
        qa_block(
            qnum=1,
            title="Two Sum",
            asked="Amazon, Google, Meta, Microsoft, Apple — classic warmup across FAANG",
            difficulty="Easy",
            pattern="Hash map · complement lookup",
            prompt=(
                "Given an array of integers nums and an integer target, return the indices of "
                "the two numbers that add up to target. Exactly one solution exists; you may not "
                "use the same element twice. This is the single most common coding-interview opener."
            ),
            sections=[
                (
                    "How to think about it",
                    "<p>Brute force checks every pair in O(n²). The interview insight: for each value "
                    "<code>x</code>, the partner you need is <code>target - x</code>. If you remember "
                    "every value you have already seen in a map from value → index, each new number "
                    "becomes one hash lookup. Store a number <em>after</em> you check for its partner "
                    "so you never pair an element with itself.</p>",
                ),
                (
                    "Solution (Python)",
                    code_block(
                        "python",
                        """def two_sum(nums, target):
    seen = {}  # value -> index
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i
    return []""",
                    ),
                ),
                (
                    "Solution (Java)",
                    code_block(
                        "java",
                        """int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> seen = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int need = target - nums[i];
        if (seen.containsKey(need)) {
            return new int[]{seen.get(need), i};
        }
        seen.put(nums[i], i);
    }
    return new int[]{};
}""",
                    ),
                ),
                (
                    "Complexity & follow-ups",
                    "<p><strong>Time O(n), space O(n).</strong> Follow-ups interviewers love: return "
                    "all pairs (use a multiset / frequency map); sorted array variant (two pointers, "
                    "O(1) extra space); what if the array is a stream?</p>",
                ),
            ],
        )
    )

    q.append(
        qa_block(
            qnum=2,
            title="Longest Substring Without Repeating Characters",
            asked="Amazon, Google, Meta, Microsoft — Blind 75 staple",
            difficulty="Medium",
            pattern="Sliding window · last-seen index",
            prompt=(
                "Given a string s, find the length of the longest substring without repeating "
                "characters. Example: \"abcabcbb\" → 3 (\"abc\")."
            ),
            sections=[
                (
                    "How to think about it",
                    "<p>Maintain a window <code>[left, right]</code> that is always duplicate-free. "
                    "Advance <code>right</code>. When <code>s[right]</code> was already inside the "
                    "window, jump <code>left</code> past its previous index. Track the best window "
                    "length. A map from character → last index avoids shrinking one-by-one.</p>",
                ),
                (
                    "Solution (Python)",
                    code_block(
                        "python",
                        """def length_of_longest_substring(s):
    last = {}
    left = best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best""",
                    ),
                ),
                (
                    "Complexity & traps",
                    "<p><strong>Time O(n), space O(min(n, alphabet)).</strong> Trap: only move "
                    "<code>left</code> forward when the previous occurrence is still inside the "
                    "window (<code>last[ch] &gt;= left</code>). Empty string and all-unique strings "
                    "are easy edge cases to miss under pressure.</p>",
                ),
            ],
        )
    )

    q.append(
        qa_block(
            qnum=3,
            title="Merge Intervals",
            asked="Amazon, Google, Meta, Microsoft — scheduling / calendar rounds",
            difficulty="Medium",
            pattern="Sort + linear merge",
            prompt=(
                "Given an array of intervals where intervals[i] = [start_i, end_i], merge all "
                "overlapping intervals and return an array of the non-overlapping intervals that "
                "cover the input exactly."
            ),
            sections=[
                (
                    "How to think about it",
                    "<p>Sort by start time. Walk left to right keeping a \"current\" interval. If "
                    "the next interval starts before or at the current end, extend the end "
                    "(take max). Otherwise push current and start a new one. Sorting is what makes "
                    "the single pass correct.</p>",
                ),
                (
                    "Solution (Python)",
                    code_block(
                        "python",
                        """def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    out = [intervals[0][:]]
    for start, end in intervals[1:]:
        if start <= out[-1][1]:
            out[-1][1] = max(out[-1][1], end)
        else:
            out.append([start, end])
    return out""",
                    ),
                ),
                (
                    "Complexity & follow-ups",
                    "<p><strong>Time O(n log n), space O(n).</strong> Follow-ups: insert a new "
                    "interval into an already-merged list; find the minimum number of meeting rooms "
                    "(sweep line / heap of end times); check if a person can attend all meetings.</p>",
                ),
            ],
        )
    )

    q.append(
        qa_block(
            qnum=4,
            title="LRU Cache",
            asked="Amazon, Google, Meta, Apple, Microsoft — most cross-company design+code problem",
            difficulty="Medium",
            pattern="Hash map + doubly linked list",
            prompt=(
                "Design a data structure that follows the constraints of a Least Recently Used "
                "(LRU) cache. Implement get(key) and put(key, value) both in O(1) average time. "
                "When capacity is exceeded, evict the least recently used key."
            ),
            sections=[
                (
                    "How to think about it",
                    "<p>Hash map alone gives O(1) get but not O(1) eviction order. Doubly linked "
                    "list alone gives O(1) move-to-front if you already have the node. Compose "
                    "them: map key → node; list ordered most-recent at head, least-recent at tail. "
                    "On get/put hit: unlink node and insert at head. On capacity overflow: remove "
                    "tail and delete its map entry.</p>",
                ),
                (
                    "Solution (Python)",
                    code_block(
                        "python",
                        """class Node:
    __slots__ = ("key", "val", "prev", "next")
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.map = {}
        self.head, self.tail = Node(), Node()
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)
        self._add_front(node)
        return node.val

    def put(self, key, value):
        if key in self.map:
            self._remove(self.map[key])
        node = Node(key, value)
        self.map[key] = node
        self._add_front(node)
        if len(self.map) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]""",
                    ),
                ),
                (
                    "What interviewers listen for",
                    "<p>Say out loud why both structures are needed. Handle capacity 1, update of "
                    "an existing key (must refresh recency without growing size), and get miss "
                    "returning -1. In Python, <code>collections.OrderedDict</code> is acceptable "
                    "if you explain move_to_end — many interviewers still want the list drawn.</p>",
                ),
            ],
        )
    )

    q.append(
        qa_block(
            qnum=5,
            title="Number of Islands",
            asked="Amazon, Google, Meta — grid / flood-fill classic",
            difficulty="Medium",
            pattern="DFS / BFS on grid",
            prompt=(
                "Given an m × n binary grid where '1' is land and '0' is water, return the number "
                "of islands. An island is formed by connecting adjacent lands horizontally or "
                "vertically (not diagonally)."
            ),
            sections=[
                (
                    "How to think about it",
                    "<p>Scan the grid. Each time you find an unvisited '1', you have discovered a "
                    "new island — increment the count, then flood-fill (DFS or BFS) to mark every "
                    "connected '1' as visited (flip to '0' or use a visited set). Never revisit.</p>",
                ),
                (
                    "Solution (Python)",
                    code_block(
                        "python",
                        """def num_islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])

    def dfs(r, c):
        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            dfs(r + dr, c + dc)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                dfs(r, c)
    return count""",
                    ),
                ),
                (
                    "Complexity & variants",
                    "<p><strong>Time O(m·n), space O(m·n)</strong> worst-case recursion / queue. "
                    "Variants: max area of island; number of closed islands; surrounded regions; "
                    "Pacific Atlantic water flow. Prefer BFS if recursion depth worries the interviewer.</p>",
                ),
            ],
        )
    )

    q.append(
        qa_block(
            qnum=6,
            title="Course Schedule (can finish all courses?)",
            asked="Amazon, Google, Meta, Intuit — topological sort / cycle detection",
            difficulty="Medium",
            pattern="Graph · Kahn's BFS or DFS cycle detect",
            prompt=(
                "There are numCourses labeled 0..n-1. prerequisites[i] = [a, b] means you must "
                "take b before a. Return true if you can finish all courses (i.e. the graph has "
                "no cycle)."
            ),
            sections=[
                (
                    "How to think about it",
                    "<p>Model courses as nodes and prerequisites as directed edges b → a. You can "
                    "finish iff the graph is a DAG. Kahn's algorithm: compute indegrees, enqueue "
                    "nodes with indegree 0, repeatedly take a node and reduce neighbors' indegrees. "
                    "If you process all nodes, there is no cycle.</p>",
                ),
                (
                    "Solution (Python)",
                    code_block(
                        "python",
                        """from collections import deque, defaultdict

def can_finish(num_courses, prerequisites):
    graph = defaultdict(list)
    indeg = [0] * num_courses
    for a, b in prerequisites:
        graph[b].append(a)
        indeg[a] += 1
    q = deque([i for i in range(num_courses) if indeg[i] == 0])
    taken = 0
    while q:
        cur = q.popleft()
        taken += 1
        for nxt in graph[cur]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)
    return taken == num_courses""",
                    ),
                ),
                (
                    "Follow-ups",
                    "<p>Course Schedule II: return any valid order (the Kahn visit order). Detect "
                    "which courses form the cycle. Weighted version → shortest path / DP on DAG.</p>",
                ),
            ],
        )
    )

    q.append(
        qa_block(
            qnum=7,
            title="Coin Change",
            asked="Amazon, Meta, Google — unbounded knapsack DP",
            difficulty="Medium",
            pattern="Dynamic programming · bottom-up",
            prompt=(
                "You are given coins of different denominations and a total amount. Return the "
                "fewest number of coins needed to make that amount. If impossible, return -1. "
                "You may use each coin unlimited times."
            ),
            sections=[
                (
                    "How to think about it",
                    "<p>Let <code>dp[x]</code> be the fewest coins to make amount x. "
                    "<code>dp[0] = 0</code>. For each amount x from 1..amount, try every coin c: "
                    "if x ≥ c, candidate is <code>dp[x - c] + 1</code>. Take the minimum. This is "
                    "unbounded knapsack — order of loops (amount outer, coins inner) is the usual "
                    "interview form.</p>",
                ),
                (
                    "Solution (Python)",
                    code_block(
                        "python",
                        """def coin_change(coins, amount):
    INF = amount + 1
    dp = [0] + [INF] * amount
    for x in range(1, amount + 1):
        for c in coins:
            if c <= x:
                dp[x] = min(dp[x], dp[x - c] + 1)
    return dp[amount] if dp[amount] != INF else -1""",
                    ),
                ),
                (
                    "Complexity & traps",
                    "<p><strong>Time O(amount · |coins|), space O(amount).</strong> Do not confuse "
                    "with Coin Change II (number of combinations). Greedy fails for arbitrary "
                    "denominations — mention that and justify DP.</p>",
                ),
            ],
        )
    )

    q.append(
        qa_block(
            qnum=8,
            title="Word Ladder",
            asked="Google, LinkedIn, Amazon — BFS shortest path in word graph",
            difficulty="Hard",
            pattern="BFS · implicit graph",
            prompt=(
                "Given beginWord, endWord, and a wordList, find the length of the shortest "
                "transformation sequence from beginWord to endWord where each step changes "
                "exactly one letter and every intermediate word is in wordList. Return 0 if "
                "impossible."
            ),
            sections=[
                (
                    "How to think about it",
                    "<p>Each word is a node; an edge exists if Hamming distance is 1. The answer "
                    "is shortest path length (number of words in the path). BFS from beginWord "
                    "guarantees shortest. Optimize neighbor generation with a set of remaining "
                    "words, or wildcard buckets (\"h*t\" → hot, hit).</p>",
                ),
                (
                    "Solution (Python)",
                    code_block(
                        "python",
                        """from collections import deque

def ladder_length(begin_word, end_word, word_list):
    words = set(word_list)
    if end_word not in words:
        return 0
    q = deque([(begin_word, 1)])
    while q:
        word, dist = q.popleft()
        if word == end_word:
            return dist
        for i in range(len(word)):
            for ch in "abcdefghijklmnopqrstuvwxyz":
                nxt = word[:i] + ch + word[i + 1 :]
                if nxt in words:
                    words.remove(nxt)
                    q.append((nxt, dist + 1))
    return 0""",
                    ),
                ),
                (
                    "Interview tips",
                    "<p>Removing a word when enqueued prevents revisits. Bidirectional BFS is a "
                    "strong follow-up for large dictionaries. Mention time O(N · L · 26) where L "
                    "is word length.</p>",
                ),
            ],
        )
    )

    q.append(
        qa_block(
            qnum=9,
            title="Serialize and Deserialize Binary Tree",
            asked="Meta (Facebook), Amazon, Microsoft — tree encoding classic",
            difficulty="Hard",
            pattern="BFS / preorder with null markers",
            prompt=(
                "Design an algorithm to serialize a binary tree to a string and deserialize "
                "that string back to the same tree structure. There is no restriction on the "
                "format — only that the pair of operations is invertible."
            ),
            sections=[
                (
                    "How to think about it",
                    "<p>Level-order (BFS) with explicit null markers is interview-friendly and "
                    "matches LeetCode's format. Serialize: queue traversal, append values / \"#\". "
                    "Deserialize: rebuild nodes in the same order, wiring left/right children as "
                    "you consume the token stream.</p>",
                ),
                (
                    "Solution (Python)",
                    code_block(
                        "python",
                        """from collections import deque

class Codec:
    def serialize(self, root):
        if not root:
            return ""
        q, out = deque([root]), []
        while q:
            node = q.popleft()
            if node:
                out.append(str(node.val))
                q.append(node.left)
                q.append(node.right)
            else:
                out.append("#")
        return ",".join(out)

    def deserialize(self, data):
        if not data:
            return None
        vals = data.split(",")
        root = TreeNode(int(vals[0]))
        q = deque([root])
        i = 1
        while q:
            node = q.popleft()
            if vals[i] != "#":
                node.left = TreeNode(int(vals[i]))
                q.append(node.left)
            i += 1
            if vals[i] != "#":
                node.right = TreeNode(int(vals[i]))
                q.append(node.right)
            i += 1
        return root""",
                    ),
                ),
                (
                    "What to say",
                    "<p>Discuss delimiter choice, empty tree, and single-node trees. Preorder with "
                    "nulls also works and uses less queue memory. Do not claim compression — "
                    "correctness and clarity beat clever encodings.</p>",
                ),
            ],
        )
    )

    q.append(
        qa_block(
            qnum=10,
            title="Trapping Rain Water",
            asked="Amazon, Google, Bloomberg — two pointers / monotonic stack",
            difficulty="Hard",
            pattern="Two pointers · left/right max",
            prompt=(
                "Given n non-negative integers representing an elevation map where the width of "
                "each bar is 1, compute how much water it can trap after raining."
            ),
            sections=[
                (
                    "How to think about it",
                    "<p>Water above index i is limited by the shorter of the tallest bar to the "
                    "left and the tallest to the right, minus height[i]. Two-pointer form: "
                    "maintain left_max and right_max while walking from both ends. Always advance "
                    "the side with the smaller max — that side's trapped water is fully determined.</p>",
                ),
                (
                    "Solution (Python)",
                    code_block(
                        "python",
                        """def trap(height):
    if not height:
        return 0
    lo, hi = 0, len(height) - 1
    left_max = right_max = water = 0
    while lo < hi:
        if height[lo] < height[hi]:
            left_max = max(left_max, height[lo])
            water += left_max - height[lo]
            lo += 1
        else:
            right_max = max(right_max, height[hi])
            water += right_max - height[hi]
            hi -= 1
    return water""",
                    ),
                ),
                (
                    "Complexity",
                    "<p><strong>Time O(n), space O(1).</strong> Prefix/suffix max arrays are the "
                    "clearer O(n) space version — start there if two pointers feel magical, then "
                    "optimize. Monotonic stack is another valid O(n) approach.</p>",
                ),
            ],
        )
    )

    return q


def cp_lab_body() -> str:
    intro = """<p>These ten problems show up constantly in FAANG and late-stage startup coding rounds
(Blind 75 / NeetCode frequency lists, Amazon online assessments, Google phone screens, Meta onsites).
Each expandable card has the prompt, how to reason under a 25–40 minute clock, working code, and the
follow-ups interviewers actually ask.</p>
<p class="drill-intro">Tip: say the pattern name out loud before coding — hash map, sliding window,
topo sort, BFS shortest path. Interviewers grade the narrative as much as the code.</p>
"""
    return intro + "\n".join(cp_questions())


def cp_chapter_drills() -> dict[str, str]:
    """Per-chapter mini drills injected into topic pages."""
    return {
        "03-arrays": drill_section(
            "Interview drill",
            "Questions interviewers actually ask when this chapter's pattern is the signal.",
            [
                qa_block(
                    qnum=1,
                    title="Two Sum",
                    asked="Amazon, Google, Meta",
                    difficulty="Easy",
                    pattern="Hash map",
                    prompt="Return indices of two numbers that add to target. One solution guaranteed.",
                    sections=[
                        (
                            "Approach",
                            "<p>One pass: for each x check if target−x is in a map of seen values; "
                            "else store x→index. O(n) time / space. Full solution in the "
                            "<a href=\"interview-cp.html\">Coding Interview Lab</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Group Anagrams",
                    asked="Amazon, Meta, Uber",
                    difficulty="Medium",
                    pattern="Hash map · sorted key / count key",
                    prompt="Group strings that are anagrams of each other.",
                    sections=[
                        (
                            "Approach",
                            "<p>Key each word by sorted characters (or a 26-count tuple). Append "
                            "into a map of key → list. Return the map values. O(n · k log k) with "
                            "sort keys, or O(n · k) with count keys.</p>"
                            + code_block(
                                "python",
                                """from collections import defaultdict

def group_anagrams(strs):
    buckets = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))
        buckets[key].append(s)
    return list(buckets.values())""",
                            ),
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Top K Frequent Elements",
                    asked="Amazon, Google, Meta",
                    difficulty="Medium",
                    pattern="Hash map + heap / bucket sort",
                    prompt="Return the k most frequent elements in an integer array.",
                    sections=[
                        (
                            "Approach",
                            "<p>Count frequencies, then either push into a size-k min-heap "
                            "(O(n log k)) or bucket-sort by frequency (O(n)). Interviewers often "
                            "ask you to beat a full sort.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Product of Array Except Self",
                    asked="Amazon, Meta, Apple",
                    difficulty="Medium",
                    pattern="Prefix / suffix products",
                    prompt="Return an array answer where answer[i] is the product of all elements "
                    "except nums[i], without using division, in O(n).",
                    sections=[
                        (
                            "Approach",
                            "<p>Left-to-right prefix products into the output, then a right-running "
                            "suffix multiplier. Two passes, O(1) extra space beyond the output.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Longest Consecutive Sequence",
                    asked="Google, Amazon",
                    difficulty="Medium",
                    pattern="Hash set",
                    prompt="Find the length of the longest consecutive elements sequence in O(n).",
                    sections=[
                        (
                            "Approach",
                            "<p>Put numbers in a set. Only start a streak when num−1 is absent. "
                            "Walk upward counting. Each number enters a streak at most once → O(n).</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-cp.html",
        ),
        "05-sliding-window": drill_section(
            "Interview drill",
            "Sliding-window problems are Amazon and Meta favorites for medium rounds.",
            [
                qa_block(
                    qnum=1,
                    title="Longest Substring Without Repeating Characters",
                    asked="Amazon, Google, Meta",
                    difficulty="Medium",
                    pattern="Variable window",
                    prompt="Length of longest substring with all unique characters.",
                    sections=[
                        (
                            "Approach",
                            "<p>Expand right; when a duplicate appears inside the window, jump left "
                            "past its last index. Track max length. See "
                            "<a href=\"interview-cp.html\">Coding Interview Lab Q2</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Minimum Window Substring",
                    asked="Meta, Amazon, LinkedIn",
                    difficulty="Hard",
                    pattern="Variable window · need/have counts",
                    prompt="Smallest substring of s that covers all characters in t (including duplicates).",
                    sections=[
                        (
                            "Approach",
                            "<p>Expand until the window satisfies t's counts, then shrink from the "
                            "left while still valid, recording the best span. Use need/have counters "
                            "so validation is O(1).</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Longest Repeating Character Replacement",
                    asked="Google, Amazon",
                    difficulty="Medium",
                    pattern="Window · max frequency",
                    prompt="Longest substring you can get by replacing at most k characters.",
                    sections=[
                        (
                            "Approach",
                            "<p>Window is valid while <code>window_len - max_freq ≤ k</code>. "
                            "Expand right; shrink left when invalid. You never need to decrease "
                            "max_freq for the answer to stay correct.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Permutation in String",
                    asked="Microsoft, Amazon",
                    difficulty="Medium",
                    pattern="Fixed window · frequency match",
                    prompt="Return true if s2 contains a permutation of s1.",
                    sections=[
                        (
                            "Approach",
                            "<p>Fixed window of len(s1) on s2; compare character counts (or a "
                            "diff counter that hits zero when matched).</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Max Consecutive Ones III",
                    asked="Facebook, Google",
                    difficulty="Medium",
                    pattern="Window · at most k zeros",
                    prompt="Longest subarray with at most k zeros (you may flip those zeros to ones).",
                    sections=[
                        (
                            "Approach",
                            "<p>Expand right; count zeros in the window; while zeros &gt; k, advance "
                            "left. Track max window length.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-cp.html",
        ),
        "12-graphs": drill_section(
            "Interview drill",
            "Graph rounds usually mean BFS/DFS on grids or adjacency lists — not fancy theory.",
            [
                qa_block(
                    qnum=1,
                    title="Number of Islands",
                    asked="Amazon, Google, Meta",
                    difficulty="Medium",
                    pattern="DFS / BFS flood fill",
                    prompt="Count connected components of '1's in a grid.",
                    sections=[
                        (
                            "Approach",
                            "<p>On each unvisited land cell, increment and flood-fill. "
                            "<a href=\"interview-cp.html\">Lab Q5</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Course Schedule",
                    asked="Amazon, Google",
                    difficulty="Medium",
                    pattern="Topological sort",
                    prompt="Can you finish all courses given prerequisite pairs?",
                    sections=[
                        (
                            "Approach",
                            "<p>Detect a cycle in a directed graph via Kahn BFS or DFS colors. "
                            "<a href=\"interview-cp.html\">Lab Q6</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Clone Graph",
                    asked="Facebook, Amazon",
                    difficulty="Medium",
                    pattern="BFS/DFS + hashmap",
                    prompt="Deep-copy a connected undirected graph of nodes with neighbor lists.",
                    sections=[
                        (
                            "Approach",
                            "<p>Map old node → new node. BFS/DFS: create clone on first visit, "
                            "then wire neighbor clones from the map.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Word Ladder",
                    asked="Google, LinkedIn",
                    difficulty="Hard",
                    pattern="BFS shortest path",
                    prompt="Shortest word transformation changing one letter at a time.",
                    sections=[
                        (
                            "Approach",
                            "<p>BFS over the word set; remove words when enqueued. "
                            "<a href=\"interview-cp.html\">Lab Q8</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Pacific Atlantic Water Flow",
                    asked="Google, Amazon",
                    difficulty="Medium",
                    pattern="Multi-source DFS/BFS",
                    prompt="Cells from which water can flow to both Pacific and Atlantic oceans.",
                    sections=[
                        (
                            "Approach",
                            "<p>Flood inland from both ocean borders (water can \"climb\" to "
                            "higher-or-equal cells). Intersection of the two reachable sets.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-cp.html",
        ),
        "13-dp": drill_section(
            "Interview drill",
            "Say the state, the transition, and the base case before you write a loop.",
            [
                qa_block(
                    qnum=1,
                    title="Coin Change",
                    asked="Amazon, Meta",
                    difficulty="Medium",
                    pattern="Unbounded knapsack",
                    prompt="Fewest coins to make amount (or -1).",
                    sections=[
                        (
                            "Approach",
                            "<p>dp[x] = min over coins of dp[x−c]+1. "
                            "<a href=\"interview-cp.html\">Lab Q7</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="House Robber",
                    asked="Amazon, Google, Apple",
                    difficulty="Medium",
                    pattern="1D DP · choose / skip",
                    prompt="Max money without robbing two adjacent houses.",
                    sections=[
                        (
                            "Approach",
                            "<p>dp[i] = max(dp[i−1], dp[i−2] + nums[i]). Roll two variables for "
                            "O(1) space.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Longest Increasing Subsequence",
                    asked="Google, Amazon",
                    difficulty="Medium",
                    pattern="Patience sorting / DP",
                    prompt="Length of the longest strictly increasing subsequence.",
                    sections=[
                        (
                            "Approach",
                            "<p>O(n²) DP is fine to start; O(n log n) maintains tails of increasing "
                            "subsequences with binary search — mention both.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Word Break",
                    asked="Facebook, Amazon, Uber",
                    difficulty="Medium",
                    pattern="DP · substring check",
                    prompt="Can s be segmented into a space-separated sequence of dictionary words?",
                    sections=[
                        (
                            "Approach",
                            "<p>dp[i] true if some dp[j] and s[j:i] in dict. Put words in a set; "
                            "optionally limit inner loop by max word length.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Unique Paths",
                    asked="Amazon, Bloomberg",
                    difficulty="Medium",
                    pattern="Grid DP",
                    prompt="Robot goes only right/down on m×n grid — how many paths to bottom-right?",
                    sections=[
                        (
                            "Approach",
                            "<p>dp[r][c] = dp[r−1][c] + dp[r][c−1], or combinatorial "
                            "C(m+n−2, m−1). Obstacles variant adds a zeroing rule.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-cp.html",
        ),
        "15-intervals": drill_section(
            "Interview drill",
            "Interval problems almost always start with sort-by-start (or a sweep line).",
            [
                qa_block(
                    qnum=1,
                    title="Merge Intervals",
                    asked="Amazon, Google, Meta",
                    difficulty="Medium",
                    pattern="Sort + merge",
                    prompt="Merge all overlapping intervals.",
                    sections=[
                        (
                            "Approach",
                            "<p>Sort by start; extend or append. "
                            "<a href=\"interview-cp.html\">Lab Q3</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Insert Interval",
                    asked="Google, LinkedIn",
                    difficulty="Medium",
                    pattern="Linear scan merge",
                    prompt="Insert a new interval into a sorted non-overlapping list and merge.",
                    sections=[
                        (
                            "Approach",
                            "<p>Add all intervals fully left of new; merge overlaps; append the rest. "
                            "O(n), no full resorted needed.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Meeting Rooms II",
                    asked="Facebook, Amazon, Bloomberg",
                    difficulty="Medium",
                    pattern="Sweep / min-heap of ends",
                    prompt="Minimum number of conference rooms required.",
                    sections=[
                        (
                            "Approach",
                            "<p>Sort starts; keep a min-heap of end times. If next start ≥ earliest "
                            "end, reuse a room (pop); else allocate (push). Heap size is the answer.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Non-overlapping Intervals",
                    asked="Amazon, Microsoft",
                    difficulty="Medium",
                    pattern="Greedy by end time",
                    prompt="Minimum number of intervals to remove to make the rest non-overlapping.",
                    sections=[
                        (
                            "Approach",
                            "<p>Sort by end; greedily keep an interval if it starts ≥ last kept end. "
                            "Removals = n − kept.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Employee Free Time",
                    asked="Airbnb, Google",
                    difficulty="Hard",
                    pattern="Merge all busy intervals",
                    prompt="Given employees' busy intervals, return common free gaps.",
                    sections=[
                        (
                            "Approach",
                            "<p>Flatten and merge all busy intervals; gaps between merged busy "
                            "blocks are free time.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-cp.html",
        ),
        "08-linked-lists": drill_section(
            "Interview drill",
            "Linked-list interviews reward pointer diagrams — draw before you mutate.",
            [
                qa_block(
                    qnum=1,
                    title="LRU Cache",
                    asked="Every FAANG — highest cross-company frequency",
                    difficulty="Medium",
                    pattern="Hash + doubly linked list",
                    prompt="O(1) get/put with LRU eviction.",
                    sections=[
                        (
                            "Approach",
                            "<p>Map to nodes; move-to-front on access; evict tail. "
                            "<a href=\"interview-cp.html\">Lab Q4</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Reverse Linked List",
                    asked="Amazon, Microsoft, Apple",
                    difficulty="Easy",
                    pattern="Three pointers",
                    prompt="Reverse a singly linked list iteratively and recursively.",
                    sections=[
                        (
                            "Approach",
                            "<p>prev/curr/next walk. Recursion: reverse rest, then "
                            "head.next.next = head; head.next = None.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Detect Cycle / Linked List Cycle II",
                    asked="Amazon, Google",
                    difficulty="Medium",
                    pattern="Floyd tortoise & hare",
                    prompt="Detect a cycle; return the node where the cycle begins.",
                    sections=[
                        (
                            "Approach",
                            "<p>Slow/fast meet ⇒ cycle. Reset one pointer to head; advance both "
                            "one step — they meet at the entrance.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Merge Two Sorted Lists",
                    asked="Amazon, Microsoft",
                    difficulty="Easy",
                    pattern="Dummy head",
                    prompt="Merge two sorted lists into one sorted list.",
                    sections=[
                        (
                            "Approach",
                            "<p>Dummy node; always attach the smaller head; append leftovers.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Copy List with Random Pointer",
                    asked="Facebook, Amazon",
                    difficulty="Medium",
                    pattern="Hash map or interleave nodes",
                    prompt="Deep copy a list where each node has next and random pointers.",
                    sections=[
                        (
                            "Approach",
                            "<p>Map old→new then wire next/random; or interleave cloned nodes "
                            "in-place then split — explain both.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-cp.html",
        ),
        "04-two-pointers": drill_section(
            "Interview drill",
            "Two pointers shine on sorted arrays and \"container\" geometry problems.",
            [
                qa_block(
                    qnum=1,
                    title="3Sum",
                    asked="Amazon, Facebook, Microsoft",
                    difficulty="Medium",
                    pattern="Sort + two pointers",
                    prompt="Find all unique triplets that sum to zero.",
                    sections=[
                        (
                            "Approach",
                            "<p>Sort; fix i; two-pointer on the rest. Skip duplicates for i/lo/hi.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Container With Most Water",
                    asked="Amazon, Google, Bloomberg",
                    difficulty="Medium",
                    pattern="Opposite ends",
                    prompt="Max area of water between two vertical lines.",
                    sections=[
                        (
                            "Approach",
                            "<p>Start at ends; move the shorter line inward — only that move can "
                            "increase area.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Trapping Rain Water",
                    asked="Amazon, Google",
                    difficulty="Hard",
                    pattern="Two pointers / stack",
                    prompt="How much rain water can the elevation map trap?",
                    sections=[
                        (
                            "Approach",
                            "<p>Advance the side with smaller max; water += max − height. "
                            "<a href=\"interview-cp.html\">Lab Q10</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Valid Palindrome",
                    asked="Facebook, Amazon",
                    difficulty="Easy",
                    pattern="Two pointers · skip non-alnum",
                    prompt="Is the string a palindrome ignoring non-alphanumeric characters?",
                    sections=[
                        (
                            "Approach",
                            "<p>lo/hi; skip non-alnum; compare lowercased chars.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Remove Duplicates from Sorted Array",
                    asked="Microsoft, Amazon",
                    difficulty="Easy",
                    pattern="Slow / fast writers",
                    prompt="In-place remove duplicates; return new length.",
                    sections=[
                        (
                            "Approach",
                            "<p>Slow writes unique values; fast scans. Classic write-index pattern.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-cp.html",
        ),
        "09-trees": drill_section(
            "Interview drill",
            "Tree interviews: name the traversal, then code it. Recursion is expected.",
            [
                qa_block(
                    qnum=1,
                    title="Serialize / Deserialize Binary Tree",
                    asked="Meta, Amazon",
                    difficulty="Hard",
                    pattern="BFS with null markers",
                    prompt="Encode a tree to a string and decode it back.",
                    sections=[
                        (
                            "Approach",
                            "<p>Level-order with # for nulls. "
                            "<a href=\"interview-cp.html\">Lab Q9</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Validate Binary Search Tree",
                    asked="Amazon, Google, Microsoft",
                    difficulty="Medium",
                    pattern="Bounds recursion / inorder",
                    prompt="Determine if a binary tree is a valid BST.",
                    sections=[
                        (
                            "Approach",
                            "<p>Pass (low, high) bounds down, or inorder and ensure strictly "
                            "increasing values.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Lowest Common Ancestor of a BST / Binary Tree",
                    asked="Facebook, Amazon",
                    difficulty="Medium",
                    pattern="Recursion / BST walk",
                    prompt="Find LCA of two nodes.",
                    sections=[
                        (
                            "Approach",
                            "<p>BST: walk left/right by value. General tree: recurse; if both "
                            "sides nonempty, root is LCA.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Binary Tree Level Order Traversal",
                    asked="Amazon, Microsoft",
                    difficulty="Medium",
                    pattern="BFS by level",
                    prompt="Return node values grouped by level.",
                    sections=[
                        (
                            "Approach",
                            "<p>Queue; for each level process queue.length nodes into a list.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Maximum Depth / Invert Binary Tree",
                    asked="Google, Apple (warmup)",
                    difficulty="Easy",
                    pattern="DFS recursion",
                    prompt="Compute height; or mirror the tree.",
                    sections=[
                        (
                            "Approach",
                            "<p>Depth = 1 + max(left, right). Invert = swap children then recurse "
                            "(or BFS swap).</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-cp.html",
        ),
        "07-binary-search": drill_section(
            "Interview drill",
            "Binary search interviews fail on boundary bugs — state the invariant every time.",
            [
                qa_block(
                    qnum=1,
                    title="Search in Rotated Sorted Array",
                    asked="Meta, Amazon, LinkedIn",
                    difficulty="Medium",
                    pattern="Binary search on rotated array",
                    prompt="Search target in a rotated sorted array with distinct values.",
                    sections=[
                        (
                            "Approach",
                            "<p>Find which half is sorted; if target lies in that half, search "
                            "there, else the other. O(log n).</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Find Minimum in Rotated Sorted Array",
                    asked="Amazon, Microsoft",
                    difficulty="Medium",
                    pattern="Binary search · pivot",
                    prompt="Find the minimum element in a rotated sorted array.",
                    sections=[
                        (
                            "Approach",
                            "<p>Compare mid to hi: if nums[mid] &gt; nums[hi], min is to the right; "
                            "else min is at mid or left.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Koko Eating Bananas",
                    asked="Google, Amazon",
                    difficulty="Medium",
                    pattern="Binary search on answer",
                    prompt="Minimum eating speed to finish piles within h hours.",
                    sections=[
                        (
                            "Approach",
                            "<p>Binary search speed in [1, max(pile)]. Feasibility: sum of "
                            "ceil(pile/speed) ≤ h.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Median of Two Sorted Arrays",
                    asked="Google, Adobe",
                    difficulty="Hard",
                    pattern="Binary partition",
                    prompt="Find median of two sorted arrays in O(log(m+n)).",
                    sections=[
                        (
                            "Approach",
                            "<p>Binary search partition on the smaller array so left parts have "
                            "correct count and max(left) ≤ min(right).</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Time-Based Key-Value Store",
                    asked="Google, Lyft",
                    difficulty="Medium",
                    pattern="Map + binary search timestamps",
                    prompt="set(key, value, timestamp); get(key, timestamp) → latest value ≤ time.",
                    sections=[
                        (
                            "Approach",
                            "<p>Store list of (time, value) per key (times increasing). "
                            "Binary search for rightmost time ≤ query.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-cp.html",
        ),
    }
