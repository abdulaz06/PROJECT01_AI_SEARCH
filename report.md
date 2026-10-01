# Project 1 Report: Intelligent Search Visualizer

> [!IMPORTANT]
> **AUTOGRADER COMPLIANCE INSTRUCTIONS:**
> This report is parsed automatically by the autograder. To ensure you receive full credit for your work:
> 1. **Do not modify** the section headers (`## ...`) or bold field keys (e.g., `**Name:**`, `**Selected Region:**`, `**Live Deployment URL:**`, etc.).
> 2. **Write your answers directly after** the colon `:` of each field, replacing the placeholder text completely (including the outer brackets `[` and `]`).
> 3. **Maintain the file structure**. Changing headers, bold titles, or deleting lines can cause the autograder to miss your responses and award 0 marks.

---

## Student Information 
- **Name:** Abdul Azeem Asharaf Ali
- **UID (netID):** aasha4
- **UIN:** 667352085

---

## Section 1: Selected City Region
- **Selected Region:** Illinois, USA

---

## Section 2: Map Graph Configuration
- **Total Cities Configured:** 22
- **Total Connection Edges:** 35
- **Graph Fully Connected:** Yes

---

## Section 3: Local Verification & Search Algorithms
*Check the algorithms you successfully ran and verified on your local development server by placing an `x` in the brackets (e.g., `[x]`):*
- [x] Breadth-First Search (BFS)
- [x] Depth-First Search (DFS)
- [x] Uniform Cost Search (UCS)
- [x] Iterative Deepening Search (IDS)
- [x] Greedy Best-First Search (Greedy)
- [x] A* Search (A*)

---

## Section 4: Deployed and Presentation Information
- **Deployment Platform:** Render
- **Live Deployment URL:** https://project01-ai-search-cu1z.onrender.com/
- **Video Presentation Link:** https://youtu.be/gHMlFt4gO_k

---

## Section 5: Discussion
- **Which search algorithm is best for this route finding problem?** 
For my route-finding problem, A* provides a good balance between finding the shortest route and limiting the number of cities expanded. It combines the distance already traveled with a Haversine estimate of the remaining distance. For Chicago to Champaign, A* found the same shortest route as UCS at 157.90 miles, but expanded only 11 cities compared with UCS’s 19. The Haversine heuristic provides a geographic straight-line estimate, helping guide the search toward the destination.
- **Search Efficiency (Nodes expanded/time taken comparison):** For Chicago to Champaign, Greedy expanded only 4 cities but returned a longer route of 190.44 miles. BFS found the same distance with 17 expansions, while IDS recorded 48 visits, including repeated cities from increasing its depth limit. DFS expanded 11 cities but returned the longest route at 284.10 miles, showing that fewer expansions do not necessarily mean a better route. A* and UCS both found the shortest distance, with A* requiring fewer expansions.
Approximate local execution times were 0.010 ms for DFS, 0.012 ms for BFS, 0.019 ms each for UCS and Greedy, 0.023 ms for IDS, and 0.029 ms for A*. These measurements exclude website and network delays. Although A* reduced exploration, its heuristic calculations added overhead on this small graph.
- **Link the idea of search algorithm to today Generative AI.** 
Generative AI also chooses among possible continuations when producing an answer, although its methods differ from the graph-search algorithms in this project. Greedy decoding selects the most likely next token, while beam search retains several candidate sequences. Both involve balancing computation with result quality. A possible extension of my project could use generative AI to interpret a travel request, call A* to calculate the shortest route, and explain the result in natural language.
