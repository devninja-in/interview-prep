#!/usr/bin/env python3
"""Competitive programming interview Q&As — deep, diagrammed FAANG drills."""
from __future__ import annotations

from interview_helpers import (
    bullets,
    callout,
    code_block,
    drill_section,
    figure_diagram,
    qa_block,
    steps,
)


def cp_questions() -> list[str]:
    q: list[str] = []

    q.append(
        qa_block(
            qnum=1,
            title="Two Sum",
            asked="Amazon, Google, Meta, Microsoft, Apple — classic FAANG warmup",
            difficulty="Easy",
            pattern="Hash map · complement lookup",
            prompt=(
                "Given an array of integers nums and an integer target, return the indices of "
                "the two numbers that add up to target. Exactly one solution exists; you may not "
                "use the same element twice. Narrate brute force → optimal, then code."
            ),
            sections=[
                (
                    "Clarify",
                    bullets(
                        [
                            "Return indices or values? (indices — LeetCode default)",
                            "Duplicates allowed in the array?",
                            "Negative numbers? (yes — hash map still works)",
                            "Guaranteed one answer, or return empty if none?",
                        ]
                    ),
                ),
                (
                    "Diagram",
                    figure_diagram("two-sum-walk", "Two Sum hash-map walkthrough"),
                ),
                (
                    "Step-by-step solution",
                    steps(
                        [
                            "<strong>Brute force:</strong> check every pair → O(n²). Say it, then improve.",
                            "<strong>Insight:</strong> for value <code>x</code> you need "
                            "<code>target - x</code>. Remember past values in a map value→index.",
                            "<strong>One pass:</strong> for each i, if need in map → return; else "
                            "store nums[i]→i <em>after</em> the check (avoids self-pair).",
                            "<strong>Complexity:</strong> time O(n), space O(n).",
                        ]
                    ),
                ),
                (
                    "Walkthrough table",
                    """<div class="table-wrap"><table>
<caption>nums=[2,7,11,15], target=9</caption>
<thead><tr><th>i</th><th>x</th><th>need</th><th>seen</th><th>action</th></tr></thead>
<tbody>
<tr><td>0</td><td>2</td><td>7</td><td>{}</td><td>miss → store 2→0</td></tr>
<tr><td>1</td><td>7</td><td>2</td><td>{2:0}</td><td>hit → return [0,1]</td></tr>
</tbody></table></div>""",
                ),
                (
                    "Python",
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
                    "Java",
                    code_block(
                        "java",
                        """int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> seen = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int need = target - nums[i];
        if (seen.containsKey(need)) return new int[]{seen.get(need), i};
        seen.put(nums[i], i);
    }
    return new int[]{};
}""",
                    ),
                ),
                (
                    "Follow-ups",
                    bullets(
                        [
                            "All pairs / duplicates → frequency map or multiset.",
                            "Sorted array → two pointers, O(1) extra space.",
                            "Streaming input → same map, bound memory if needed.",
                        ]
                    ),
                ),
                (
                    "Common mistakes",
                    callout(
                        "Watch for",
                        bullets(
                            [
                                "Storing before checking → pairing with self when 2x = target.",
                                "Returning values instead of indices.",
                                "Using a list scan for \"seen\" → accidental O(n²).",
                            ]
                        ),
                    ),
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
                    "Clarify",
                    bullets(
                        [
                            "ASCII / Unicode? (map works either way)",
                            "Empty string → 0",
                            "All unique → n; all same → 1",
                        ]
                    ),
                ),
                (
                    "Diagram",
                    figure_diagram("longest-substr-window", "Sliding window for unique substring"),
                ),
                (
                    "Step-by-step solution",
                    steps(
                        [
                            "Maintain window [left, right] that is always duplicate-free.",
                            "Advance right. If s[right] was seen at index ≥ left, set "
                            "left = last[ch] + 1.",
                            "Update last[ch] = right; track best = max(best, right-left+1).",
                            "Time O(n), space O(min(n, alphabet)).",
                        ]
                    ),
                ),
                (
                    "Python",
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
                    "Trap",
                    callout(
                        "Invariant",
                        "<p>Only move left when the previous occurrence is still <em>inside</em> "
                        "the window (<code>last[ch] &gt;= left</code>). Otherwise you can "
                        "accidentally shrink past a valid window.</p>",
                    ),
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
                "Given intervals[i] = [start_i, end_i], merge all overlapping intervals and "
                "return the covering non-overlapping set."
            ),
            sections=[
                (
                    "Diagram",
                    figure_diagram("merge-intervals-walk", "Merge overlapping intervals"),
                ),
                (
                    "Step-by-step solution",
                    steps(
                        [
                            "Sort by start time — required for a single pass.",
                            "Keep a \"current\" interval. If next.start ≤ current.end, "
                            "current.end = max(ends). Else push current and start new.",
                            "Touching intervals [1,2][2,3]: ask if they merge (usually yes with ≤).",
                            "Time O(n log n), space O(n).",
                        ]
                    ),
                ),
                (
                    "Python",
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
                    "Follow-ups",
                    bullets(
                        [
                            "Insert Interval into an already-merged list (O(n), no full resort).",
                            "Meeting Rooms II → min heap of end times / sweep line.",
                            "Min removals to make non-overlapping → greedy by end.",
                        ]
                    ),
                ),
            ],
        )
    )

    q.append(
        qa_block(
            qnum=4,
            title="LRU Cache",
            asked="Amazon, Google, Meta, Apple, Microsoft — highest cross-company design+code",
            difficulty="Medium",
            pattern="Hash map + doubly linked list",
            prompt=(
                "Design LRUCache with get(key) and put(key, value) in O(1) average time. "
                "Evict the least recently used key when over capacity."
            ),
            sections=[
                (
                    "Clarify",
                    bullets(
                        [
                            "Capacity ≥ 1?",
                            "get miss → -1",
                            "put on existing key updates value AND recency",
                            "Thread safety? (usually out of scope unless asked)",
                        ]
                    ),
                ),
                (
                    "Diagram",
                    figure_diagram("lru-cache", "Hash map plus doubly linked list"),
                ),
                (
                    "Step-by-step solution",
                    steps(
                        [
                            "<strong>Why both structures?</strong> Map → O(1) lookup. DLL → O(1) "
                            "reorder / evict if you already have the node pointer.",
                            "Sentinel head/tail simplify edge inserts/removes.",
                            "get hit: unlink node, insert after head (MRU), return value.",
                            "put: if key exists, remove old node; insert new at head; if "
                            "size &gt; capacity, remove tail.prev and delete from map.",
                            "Draw the list on the whiteboard before coding helpers.",
                        ]
                    ),
                ),
                (
                    "Python",
                    code_block(
                        "python",
                        """class Node:
    __slots__ = ("key", "val", "prev", "next")
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.cap, self.map = capacity, {}
        self.head, self.tail = Node(), Node()
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node):
        node.next, node.prev = self.head.next, self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node); self._add_front(node)
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
                    callout(
                        "Signal",
                        "<p>Explain composition out loud. Handle capacity 1 and update-existing "
                        "without growing size. OrderedDict is OK if you explain "
                        "<code>move_to_end</code> — many still want the list drawn.</p>",
                    ),
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
                "Given an m×n grid of '1' (land) and '0' (water), return the number of islands. "
                "Land connects 4-directionally (not diagonally)."
            ),
            sections=[
                (
                    "Diagram",
                    figure_diagram("islands-dfs", "Flood-fill islands on a grid"),
                ),
                (
                    "Step-by-step solution",
                    steps(
                        [
                            "Scan every cell. On unvisited '1', increment count.",
                            "Flood-fill (DFS or BFS) to mark the whole component visited "
                            "(flip to '0' or use a visited set).",
                            "Never revisit. Prefer BFS if recursion depth worries them.",
                            "Time O(m·n), space O(m·n) worst case.",
                        ]
                    ),
                ),
                (
                    "Python",
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
                    "Variants",
                    bullets(
                        [
                            "Max area of island",
                            "Number of closed islands",
                            "Pacific Atlantic water flow (multi-source DFS)",
                            "Surrounded regions",
                        ]
                    ),
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
            pattern="Graph · Kahn BFS or DFS colors",
            prompt=(
                "numCourses labeled 0..n-1. prerequisites[i]=[a,b] means take b before a. "
                "Return true iff you can finish all courses (DAG / no cycle)."
            ),
            sections=[
                (
                    "Diagram",
                    figure_diagram("topo-kahn", "Kahn topological sort for courses"),
                ),
                (
                    "Step-by-step solution",
                    steps(
                        [
                            "Model: directed edge b→a (b unlocks a). Finish iff DAG.",
                            "Kahn: compute indegrees; queue all indegree 0; pop and decrement "
                            "neighbors; count processed nodes.",
                            "If processed == numCourses → true; else cycle → false.",
                            "DFS alternative: 0/1/2 colors; back-edge to \"in stack\" = cycle.",
                        ]
                    ),
                ),
                (
                    "Python",
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
                    bullets(
                        [
                            "Course Schedule II → return any valid order (Kahn visit order).",
                            "Parallel semesters → longest path in DAG / level BFS.",
                        ]
                    ),
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
                "coins of various denominations, total amount. Return fewest coins to make "
                "amount, or -1 if impossible. Unlimited supply of each coin."
            ),
            sections=[
                (
                    "Diagram",
                    figure_diagram("coin-change-dp", "Bottom-up coin change DP table"),
                ),
                (
                    "Step-by-step solution",
                    steps(
                        [
                            "Define dp[x] = fewest coins to make x; dp[0]=0; else ∞.",
                            "For x from 1..amount: for each coin c≤x: "
                            "dp[x]=min(dp[x], dp[x-c]+1).",
                            "Why not greedy? Counterexample coins=[1,3,4], amount=6 → "
                            "greedy 4+1+1=3 coins, optimal 3+3=2.",
                            "Time O(amount·|coins|), space O(amount).",
                        ]
                    ),
                ),
                (
                    "Python",
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
                    "Related",
                    "<p>Coin Change II counts combinations — different transition order/"
                    "meaning. Do not confuse them in the interview.</p>",
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
                "beginWord → endWord, changing one letter at a time; each intermediate in "
                "wordList. Return length of shortest transformation sequence (words in path), "
                "or 0 if impossible."
            ),
            sections=[
                (
                    "Diagram",
                    figure_diagram("word-ladder-bfs", "BFS over one-letter neighbors"),
                ),
                (
                    "Step-by-step solution",
                    steps(
                        [
                            "Each word is a node; edge if Hamming distance 1.",
                            "BFS from beginWord; distance = words in path so far.",
                            "Neighbor gen: for each position try a–z; check set membership.",
                            "Remove word when enqueued to avoid revisits.",
                            "If endWord not in wordList → 0 immediately.",
                            "Time O(N · L · 26); bidirectional BFS is a strong follow-up.",
                        ]
                    ),
                ),
                (
                    "Python",
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
                "Design serialize(root)→string and deserialize(string)→tree. Format is your "
                "choice; the pair must be invertible."
            ),
            sections=[
                (
                    "Diagram",
                    figure_diagram("serialize-tree", "BFS serialize with null markers"),
                ),
                (
                    "Step-by-step solution",
                    steps(
                        [
                            "Pick BFS level-order with explicit '#' nulls (interview-friendly).",
                            "Serialize: queue; append values / '#'; join with commas.",
                            "Deserialize: rebuild root from first token; for each node consume "
                            "next two tokens as left/right children.",
                            "Handle empty tree and single-node trees explicitly.",
                            "Preorder+nulls also works — mention both.",
                        ]
                    ),
                ),
                (
                    "Python",
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
                "n non-negative heights (bar width 1). How much water can the elevation map "
                "trap after raining?"
            ),
            sections=[
                (
                    "Diagram",
                    figure_diagram("trap-water", "Trapped water between bars"),
                ),
                (
                    "Step-by-step solution",
                    steps(
                        [
                            "Water at i limited by min(tallest left, tallest right) − height[i].",
                            "Prefix/suffix max arrays → clear O(n) time / O(n) space version — "
                            "start here if needed.",
                            "Two pointers: maintain left_max, right_max; always advance the side "
                            "with the smaller max (that side's water is fully determined).",
                            "Time O(n), space O(1). Monotonic stack is another valid approach.",
                        ]
                    ),
                ),
                (
                    "Python",
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
                    "Why the two-pointer trick works",
                    callout(
                        "Intuition",
                        "<p>If height[lo] &lt; height[hi], the water at lo cannot be limited by "
                        "anything on the right taller than height[hi] — left_max is the binding "
                        "constraint. Symmetric for the right side.</p>",
                    ),
                ),
            ],
        )
    )

    return q


def cp_lab_body() -> str:
    from interview_cp_extra import cp_extra_questions

    intro = """
<p>This lab covers the <strong>highest-frequency coding interview problems</strong> across FAANG
and late-stage startups — sourced from 2025–2026 interview report aggregations (Blind / LeetCode
Discuss frequency lists, Amazon OAs, Google phones, Meta onsites). Each card is a full 25–40 minute
practice: clarify → diagram → steps → code → follow-ups.</p>

<p class="drill-intro"><strong>How to use it:</strong> Time yourself. Say the pattern name before
coding. After you finish, close the card and re-explain the invariant from memory.</p>

<figure class="diagram native">
<img src="../assets/diagrams/two-sum-walk.svg" alt="Two Sum walkthrough overview" loading="lazy" />
</figure>

<p class="drill-intro">Related chapters:
<a href="03-arrays.html">Arrays</a>,
<a href="05-sliding-window.html">Sliding window</a>,
<a href="08-linked-lists.html">Linked lists</a>,
<a href="12-graphs.html">Graphs</a>,
<a href="13-dp.html">DP</a>.</p>

<ul class="lab-toc">
  <li><a href="#q1"><span>Q1</span> Two Sum</a></li>
  <li><a href="#q2"><span>Q2</span> Longest substring without repeats</a></li>
  <li><a href="#q3"><span>Q3</span> Merge Intervals</a></li>
  <li><a href="#q4"><span>Q4</span> LRU Cache</a></li>
  <li><a href="#q5"><span>Q5</span> Number of Islands</a></li>
  <li><a href="#q6"><span>Q6</span> Course Schedule</a></li>
  <li><a href="#q7"><span>Q7</span> Coin Change</a></li>
  <li><a href="#q8"><span>Q8</span> Word Ladder</a></li>
  <li><a href="#q9"><span>Q9</span> Serialize / Deserialize Tree</a></li>
  <li><a href="#q10"><span>Q10</span> Trapping Rain Water</a></li>
  <li><a href="#q11"><span>Q11</span> Best Time to Buy/Sell Stock</a></li>
  <li><a href="#q12"><span>Q12</span> Minimum Window Substring</a></li>
  <li><a href="#q13"><span>Q13</span> Maximum Subarray (Kadane)</a></li>
  <li><a href="#q14"><span>Q14</span> Search in Rotated Sorted Array</a></li>
  <li><a href="#q15"><span>Q15</span> Top K Frequent Elements</a></li>
  <li><a href="#q16"><span>Q16</span> Meeting Rooms II</a></li>
  <li><a href="#q17"><span>Q17</span> Valid Parentheses</a></li>
  <li><a href="#q18"><span>Q18</span> Rotting Oranges</a></li>
  <li><a href="#q19"><span>Q19</span> Alien Dictionary</a></li>
  <li><a href="#q20"><span>Q20</span> Kth Largest Element</a></li>
</ul>
"""
    blocks = cp_questions() + cp_extra_questions(11)
    out = []
    for i, block in enumerate(blocks, start=1):
        out.append(block.replace('<details class="qa">', f'<details class="qa" id="q{i}">', 1))
    return intro + "\n".join(out)


def cp_chapter_drills() -> dict[str, str]:
    """Per-chapter mini drills — deepened, pointing at the lab."""
    return {
        "03-arrays": drill_section(
            "Interview drill — Arrays &amp; hashing",
            "Hash-map interviews reward saying the complement insight before coding.",
            [
                qa_block(
                    qnum=1,
                    title="Two Sum",
                    asked="Amazon, Google, Meta",
                    difficulty="Easy",
                    pattern="Hash map",
                    prompt="Indices of two numbers that add to target.",
                    sections=[
                        (
                            "Steps",
                            figure_diagram("two-sum-walk", "Two Sum")
                            + steps(
                                [
                                    "For each x, need = target − x.",
                                    "If need in seen → return indices; else store x.",
                                    "Store after check to avoid self-pairs.",
                                ]
                            )
                            + "<p><a href=\"interview-cp.html#q1\">Full lab Q1</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Group Anagrams",
                    asked="Amazon, Meta, Uber",
                    difficulty="Medium",
                    pattern="Hash map · sorted / count key",
                    prompt="Group strings that are anagrams.",
                    sections=[
                        (
                            "Approach",
                            code_block(
                                "python",
                                """from collections import defaultdict

def group_anagrams(strs):
    buckets = defaultdict(list)
    for s in strs:
        buckets[tuple(sorted(s))].append(s)
    return list(buckets.values())""",
                            )
                            + "<p>Count-tuple keys make it O(n·k) instead of O(n·k log k).</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Top K Frequent Elements",
                    asked="Amazon, Google, Meta",
                    difficulty="Medium",
                    pattern="Heap / bucket sort",
                    prompt="k most frequent elements.",
                    sections=[
                        (
                            "Approach",
                            "<p>Count → size-k min-heap O(n log k), or bucket by frequency O(n). "
                            "Interviewers often ask you to beat a full sort.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Product of Array Except Self",
                    asked="Amazon, Meta, Apple",
                    difficulty="Medium",
                    pattern="Prefix / suffix",
                    prompt="Products excluding self, no division, O(n).",
                    sections=[
                        (
                            "Approach",
                            "<p>Left-to-right prefix into output, then right-running suffix "
                            "multiplier. O(1) extra space beyond output.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Longest Consecutive Sequence",
                    asked="Google, Amazon",
                    difficulty="Medium",
                    pattern="Hash set",
                    prompt="Longest consecutive run in O(n).",
                    sections=[
                        (
                            "Approach",
                            "<p>Set of numbers; only start a streak when num−1 missing; walk up. "
                            "Each number enters a streak once → O(n).</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-cp.html",
        ),
        "05-sliding-window": drill_section(
            "Interview drill — Sliding window",
            "Name the invariant: what makes the window valid?",
            [
                qa_block(
                    qnum=1,
                    title="Longest Substring Without Repeating Characters",
                    asked="Amazon, Google, Meta",
                    difficulty="Medium",
                    pattern="Variable window",
                    prompt="Longest unique-char substring length.",
                    sections=[
                        (
                            "Steps",
                            figure_diagram("longest-substr-window", "Window")
                            + "<p><a href=\"interview-cp.html#q2\">Lab Q2</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Minimum Window Substring",
                    asked="Meta, Amazon, LinkedIn",
                    difficulty="Hard",
                    pattern="need/have counts",
                    prompt="Smallest window of s covering t.",
                    sections=[
                        (
                            "Approach",
                            steps(
                                [
                                    "Expand until window satisfies t's counts.",
                                    "Shrink from left while still valid; track best.",
                                    "need/have counters keep validation O(1).",
                                ]
                            ),
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Longest Repeating Character Replacement",
                    asked="Google, Amazon",
                    difficulty="Medium",
                    pattern="max frequency",
                    prompt="Longest substring with ≤ k replacements.",
                    sections=[
                        (
                            "Approach",
                            "<p>Valid while window_len − max_freq ≤ k. You need not decrease "
                            "max_freq for the answer to stay correct.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Permutation in String",
                    asked="Microsoft, Amazon",
                    difficulty="Medium",
                    pattern="Fixed window",
                    prompt="Does s2 contain a permutation of s1?",
                    sections=[
                        (
                            "Approach",
                            "<p>Fixed window of len(s1); match character counts / diff counter.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Max Consecutive Ones III",
                    asked="Facebook, Google",
                    difficulty="Medium",
                    pattern="at most k zeros",
                    prompt="Longest subarray with ≤ k zeros.",
                    sections=[
                        (
                            "Approach",
                            "<p>Expand right; while zeros &gt; k advance left; track max length.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-cp.html",
        ),
        "12-graphs": drill_section(
            "Interview drill — Graphs",
            "Grid DFS/BFS and topo sort cover most graph phone screens.",
            [
                qa_block(
                    qnum=1,
                    title="Number of Islands",
                    asked="Amazon, Google, Meta",
                    difficulty="Medium",
                    pattern="Flood fill",
                    prompt="Count land components.",
                    sections=[
                        (
                            "Steps",
                            figure_diagram("islands-dfs", "Islands")
                            + "<p><a href=\"interview-cp.html#q5\">Lab Q5</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Course Schedule",
                    asked="Amazon, Google",
                    difficulty="Medium",
                    pattern="Topo sort",
                    prompt="Can you finish all courses?",
                    sections=[
                        (
                            "Steps",
                            figure_diagram("topo-kahn", "Kahn")
                            + "<p><a href=\"interview-cp.html#q6\">Lab Q6</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Clone Graph",
                    asked="Facebook, Amazon",
                    difficulty="Medium",
                    pattern="BFS + map",
                    prompt="Deep-copy undirected graph.",
                    sections=[
                        (
                            "Approach",
                            "<p>Map old→new; BFS/DFS create clone on first visit, then wire "
                            "neighbor clones.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Word Ladder",
                    asked="Google, LinkedIn",
                    difficulty="Hard",
                    pattern="BFS shortest path",
                    prompt="Shortest one-letter word transform.",
                    sections=[
                        (
                            "Steps",
                            figure_diagram("word-ladder-bfs", "Word ladder")
                            + "<p><a href=\"interview-cp.html#q8\">Lab Q8</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Pacific Atlantic Water Flow",
                    asked="Google, Amazon",
                    difficulty="Medium",
                    pattern="Multi-source DFS",
                    prompt="Cells that can reach both oceans.",
                    sections=[
                        (
                            "Approach",
                            "<p>Flood inland from both borders; intersection of reachable sets.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-cp.html",
        ),
        "13-dp": drill_section(
            "Interview drill — DP",
            "State → transition → base case — say them before the loop.",
            [
                qa_block(
                    qnum=1,
                    title="Coin Change",
                    asked="Amazon, Meta",
                    difficulty="Medium",
                    pattern="Unbounded knapsack",
                    prompt="Fewest coins for amount.",
                    sections=[
                        (
                            "Steps",
                            figure_diagram("coin-change-dp", "Coin DP")
                            + "<p><a href=\"interview-cp.html#q7\">Lab Q7</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="House Robber",
                    asked="Amazon, Google, Apple",
                    difficulty="Medium",
                    pattern="choose / skip",
                    prompt="Max money, no adjacent houses.",
                    sections=[
                        (
                            "Approach",
                            "<p>dp[i]=max(dp[i−1], dp[i−2]+nums[i]). Roll two variables for O(1) space.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Longest Increasing Subsequence",
                    asked="Google, Amazon",
                    difficulty="Medium",
                    pattern="Patience / DP",
                    prompt="LIS length.",
                    sections=[
                        (
                            "Approach",
                            "<p>O(n²) DP fine to start; O(n log n) tails + binary search — mention both.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Word Break",
                    asked="Facebook, Amazon, Uber",
                    difficulty="Medium",
                    pattern="substring DP",
                    prompt="Can s be segmented into dictionary words?",
                    sections=[
                        (
                            "Approach",
                            "<p>dp[i] true if some dp[j] and s[j:i] in dict. Cap inner loop by max word length.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Unique Paths",
                    asked="Amazon, Bloomberg",
                    difficulty="Medium",
                    pattern="Grid DP",
                    prompt="Right/down paths on m×n grid.",
                    sections=[
                        (
                            "Approach",
                            "<p>dp[r][c]=dp[r−1][c]+dp[r][c−1], or C(m+n−2, m−1).</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-cp.html",
        ),
        "15-intervals": drill_section(
            "Interview drill — Intervals",
            "Almost always: sort by start (or sweep by time).",
            [
                qa_block(
                    qnum=1,
                    title="Merge Intervals",
                    asked="Amazon, Google, Meta",
                    difficulty="Medium",
                    pattern="Sort + merge",
                    prompt="Merge overlaps.",
                    sections=[
                        (
                            "Steps",
                            figure_diagram("merge-intervals-walk", "Merge")
                            + "<p><a href=\"interview-cp.html#q3\">Lab Q3</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Insert Interval",
                    asked="Google, LinkedIn",
                    difficulty="Medium",
                    pattern="Linear merge",
                    prompt="Insert into sorted non-overlapping list.",
                    sections=[
                        (
                            "Approach",
                            "<p>Add fully-left; merge overlaps; append rest. O(n).</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Meeting Rooms II",
                    asked="Facebook, Amazon, Bloomberg",
                    difficulty="Medium",
                    pattern="Min-heap of ends",
                    prompt="Minimum conference rooms.",
                    sections=[
                        (
                            "Approach",
                            "<p>Sort starts; heap of ends; reuse room if start ≥ earliest end. "
                            "Heap size = answer.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Non-overlapping Intervals",
                    asked="Amazon, Microsoft",
                    difficulty="Medium",
                    pattern="Greedy by end",
                    prompt="Min removals for non-overlap.",
                    sections=[
                        (
                            "Approach",
                            "<p>Sort by end; keep if start ≥ last end; removals = n − kept.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Employee Free Time",
                    asked="Airbnb, Google",
                    difficulty="Hard",
                    pattern="Merge busy",
                    prompt="Common free gaps across employees.",
                    sections=[
                        (
                            "Approach",
                            "<p>Flatten+merge all busy intervals; gaps between merges are free.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-cp.html",
        ),
        "08-linked-lists": drill_section(
            "Interview drill — Linked lists",
            "Draw pointers before you mutate — especially for LRU.",
            [
                qa_block(
                    qnum=1,
                    title="LRU Cache",
                    asked="Every FAANG",
                    difficulty="Medium",
                    pattern="Hash + DLL",
                    prompt="O(1) get/put with LRU eviction.",
                    sections=[
                        (
                            "Steps",
                            figure_diagram("lru-cache", "LRU")
                            + "<p><a href=\"interview-cp.html#q4\">Lab Q4</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Reverse Linked List",
                    asked="Amazon, Microsoft, Apple",
                    difficulty="Easy",
                    pattern="Three pointers",
                    prompt="Reverse iteratively and recursively.",
                    sections=[
                        (
                            "Approach",
                            "<p>prev/curr/next walk. Recursion: reverse rest, then "
                            "head.next.next=head; head.next=None.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Linked List Cycle II",
                    asked="Amazon, Google",
                    difficulty="Medium",
                    pattern="Floyd",
                    prompt="Return the node where the cycle begins.",
                    sections=[
                        (
                            "Approach",
                            "<p>Slow/fast meet ⇒ cycle. Reset one to head; advance both one step "
                            "→ entrance.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Merge Two Sorted Lists",
                    asked="Amazon, Microsoft",
                    difficulty="Easy",
                    pattern="Dummy head",
                    prompt="Merge two sorted lists.",
                    sections=[
                        (
                            "Approach",
                            "<p>Dummy node; always attach smaller head; append leftovers.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Copy List with Random Pointer",
                    asked="Facebook, Amazon",
                    difficulty="Medium",
                    pattern="Map or interleave",
                    prompt="Deep copy next+random list.",
                    sections=[
                        (
                            "Approach",
                            "<p>Map old→new then wire; or interleave clones in-place then split.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-cp.html",
        ),
        "04-two-pointers": drill_section(
            "Interview drill — Two pointers",
            "Sorted arrays and container geometry — state the move rule.",
            [
                qa_block(
                    qnum=1,
                    title="3Sum",
                    asked="Amazon, Facebook, Microsoft",
                    difficulty="Medium",
                    pattern="Sort + two pointers",
                    prompt="Unique triplets summing to 0.",
                    sections=[
                        (
                            "Approach",
                            "<p>Sort; fix i; two-pointer on rest; skip duplicates for i/lo/hi.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Container With Most Water",
                    asked="Amazon, Google, Bloomberg",
                    difficulty="Medium",
                    pattern="Opposite ends",
                    prompt="Max area between two lines.",
                    sections=[
                        (
                            "Approach",
                            "<p>Start at ends; move the shorter line inward — only that can improve area.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Trapping Rain Water",
                    asked="Amazon, Google",
                    difficulty="Hard",
                    pattern="Two pointers",
                    prompt="How much rain is trapped?",
                    sections=[
                        (
                            "Steps",
                            figure_diagram("trap-water", "Trap")
                            + "<p><a href=\"interview-cp.html#q10\">Lab Q10</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Valid Palindrome",
                    asked="Facebook, Amazon",
                    difficulty="Easy",
                    pattern="Skip non-alnum",
                    prompt="Palindrome ignoring non-alphanumeric?",
                    sections=[
                        (
                            "Approach",
                            "<p>lo/hi; skip non-alnum; compare lowercased.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Remove Duplicates from Sorted Array",
                    asked="Microsoft, Amazon",
                    difficulty="Easy",
                    pattern="Slow/fast writers",
                    prompt="In-place unique prefix length.",
                    sections=[
                        (
                            "Approach",
                            "<p>Slow writes uniques; fast scans.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-cp.html",
        ),
        "09-trees": drill_section(
            "Interview drill — Trees",
            "Name the traversal, then code it.",
            [
                qa_block(
                    qnum=1,
                    title="Serialize / Deserialize Binary Tree",
                    asked="Meta, Amazon",
                    difficulty="Hard",
                    pattern="BFS + nulls",
                    prompt="Encode and decode a tree.",
                    sections=[
                        (
                            "Steps",
                            figure_diagram("serialize-tree", "Serialize")
                            + "<p><a href=\"interview-cp.html#q9\">Lab Q9</a>.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Validate BST",
                    asked="Amazon, Google, Microsoft",
                    difficulty="Medium",
                    pattern="Bounds / inorder",
                    prompt="Is the tree a valid BST?",
                    sections=[
                        (
                            "Approach",
                            "<p>Pass (low, high) bounds, or inorder strictly increasing.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Lowest Common Ancestor",
                    asked="Facebook, Amazon",
                    difficulty="Medium",
                    pattern="Recursion / BST walk",
                    prompt="LCA of two nodes.",
                    sections=[
                        (
                            "Approach",
                            "<p>BST: walk by value. General: if both sides nonempty, root is LCA.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Level Order Traversal",
                    asked="Amazon, Microsoft",
                    difficulty="Medium",
                    pattern="BFS by level",
                    prompt="Values grouped by level.",
                    sections=[
                        (
                            "Approach",
                            "<p>Queue; process queue.length nodes per level into a list.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Max Depth / Invert Tree",
                    asked="Google, Apple warmup",
                    difficulty="Easy",
                    pattern="DFS",
                    prompt="Height or mirror the tree.",
                    sections=[
                        (
                            "Approach",
                            "<p>Depth=1+max(left,right). Invert=swap children then recurse.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-cp.html",
        ),
        "07-binary-search": drill_section(
            "Interview drill — Binary search",
            "State the invariant every iteration — that is the interview.",
            [
                qa_block(
                    qnum=1,
                    title="Search in Rotated Sorted Array",
                    asked="Meta, Amazon, LinkedIn",
                    difficulty="Medium",
                    pattern="Rotated binary search",
                    prompt="Find target in rotated sorted array.",
                    sections=[
                        (
                            "Approach",
                            "<p>Find which half is sorted; if target in that half, search there, else the other.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=2,
                    title="Find Minimum in Rotated Sorted Array",
                    asked="Amazon, Microsoft",
                    difficulty="Medium",
                    pattern="Pivot",
                    prompt="Minimum element after rotation.",
                    sections=[
                        (
                            "Approach",
                            "<p>Compare mid to hi: if nums[mid] &gt; nums[hi], min is right; else mid or left.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=3,
                    title="Koko Eating Bananas",
                    asked="Google, Amazon",
                    difficulty="Medium",
                    pattern="Binary search on answer",
                    prompt="Min speed to finish in h hours.",
                    sections=[
                        (
                            "Approach",
                            "<p>Search speed in [1, max(pile)]; feasible if Σ ceil(pile/speed) ≤ h.</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=4,
                    title="Median of Two Sorted Arrays",
                    asked="Google, Adobe",
                    difficulty="Hard",
                    pattern="Binary partition",
                    prompt="Median in O(log(m+n)).",
                    sections=[
                        (
                            "Approach",
                            "<p>Binary search partition on smaller array so left count is correct "
                            "and max(left) ≤ min(right).</p>",
                        ),
                    ],
                ),
                qa_block(
                    qnum=5,
                    title="Time-Based Key-Value Store",
                    asked="Google, Lyft",
                    difficulty="Medium",
                    pattern="Map + bisect",
                    prompt="get(key,t) → latest value with time ≤ t.",
                    sections=[
                        (
                            "Approach",
                            "<p>Per key, list of (time,value) ascending; bisect rightmost ≤ t.</p>",
                        ),
                    ],
                ),
            ],
            lab_href="interview-cp.html",
        ),
    }
