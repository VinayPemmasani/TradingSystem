# RESEARCH: AI-style vs hot-path C++ (sourced framing)

Pages fetched 2026-11-19. Quotes are short excerpts as the pages give them. [n] = link list at the end.

## 1. Stroustrup on AI-generated C++
- eFinancialCareers, Alex McMurray, **2 June 2026** [1], reporting a podcast from "last month" (May 2026; the podcast is not named). Direct quotes: "the examples I've seen of attempts for AI to generate code in this domain have not been successful." / "If an AI writes it, you don't actually know where it has changed". Reported speech: "Stroustrup also said that AI-generated low latency C++ code is "bloated"". English is "often very ambiguous"; C++ is "precise". Do not put "bloated, buggy, insecure" in quotation marks as his words. Only "bloated" is attributed to him, and the bug and security points are the reporter's paraphrase.
- NewsBytes, **20 May 2026** [2]: paraphrase only, with no direct quotes and no venue. Use it only as corroboration.
- Susquehanna: Business Wire, **6 Aug 2026** [3]. He joined as Technical Fellow: "Financial software places extraordinary demands on performance, reliability, and maintainability". Also reported in [4]. **Correction to BRIEF:** the eFC article is dated 2 June, not 6 Aug, and does not mention the hire. The 6 Aug date belongs to the Business Wire release. That release says nothing about AI.

## 2. Measured evidence: the "Google 5-8%" study (checked, with caveats)
AI Weekly [5] cites arXiv 2608.06640 [6]: Tran, Lewis, ..., Hashemi, Ranganathan (Google affiliation), "Characterizing the Quality Profile of AI-Generated C++ in Production", 6 Aug 2026. It studies 3.52M code changes from Apr 2025 to Apr 2026 in one large monorepo. The paper anonymises the company and names no models.
- What "5-8%" actually is [6]: an observational function-level cohort comparison, normalised to total application compute. AI-heavy functions grew to about 1.31x baseline **CPU** against 1.25x for human-written functions ("an approximate 5% relative increase"). For **heap memory** the figures are 1.36x against 1.25x ("approximate 8%"). The authors call these associations, not causal effects. **The study does not measure latency or HFT code.**
- Relevant findings: "copy and allocation overheads". The Copy & Allocation Overhead category has a rate ratio of 1.39 (AI vs human), and `runtime-missing-move` makes up 51.6% of it. AI code has about 2x the `use-emplace` and `inefficient-map` warnings, about 2x as many explicit loops, and about 0.4x the std:: usage. Correctness & Safety is **0.94**, meaning *fewer* findings in AI code than in human code. Taxonomy-informed feedback cut targeted warnings by 11.1%, measured on a benchmark. On screen, say "about 5% more CPU, about 8% more memory, observational".

## 3. Practitioner principles (-> slugs)
| Principle (source) | Slugs |
|---|---|
| "Most of the time, you don't want node containers"; std::map vs sorted vector, reversed so the best price sits at the end; "we need a hash table" for order IDs; ~1000 levels per side (Gross [7]) | 02, 05, 01 |
| Open-addressing `array_map` find: 7-9 ns, against 14-24 ns for `std::unordered_map`; IPC 1.6 vs 0.67 (Cook [8]) | 01 |
| "Allocations are costly"; use "a pool of preallocated objects"; glibc free has "400 lines of book-keeping" (Cook [8]). Pre-allocate at startup and "avoid dynamic containers on the hot path" (DE [9]) | 04, 05, 03 |
| Exceptions are "zero cost if they don't throw"; used for control flow they cost "at least 1.5us" (Cook [8]) | 07 |
| Virtuals "(and even simple branches) can be expensive"; choose the type at compile time with templates. "std::function may allocate"; use lambdas or inplace_function (Cook [8]; Gross [7]) | 08 |
| Branchless binary search: "multiplication (by 1) is needed for GCC to generate CMOV" (Gross [7]); keep error handling out of line in a cold path (Cook [8]; Gross [7]) | 13 |
| Trace with `__rdtsc()` into a queue and let a separate thread write it out (Gross [7]); a complex logging function marked `noinline` (Cook [8]); put logging on a separate NUMA node (DE [9]) | 09 |
| "Use lock-free SPSC queues" (DE [9]). FastQueue: counters with `alignas(CACHE_LINE_SIZE)`, cached counters, "readers don't affect the writer"; one writer only (Gross [7]) | 10, 12 |
| Producer stores with `memory_order_release`, consumer loads with `acquire` (Gross [7]) | 11 |
| "Multiple threads writing to the same cacheline will get expensive" (Cook [8]); "False sharing between threads on the same cache line" (DE [9]) | 12 |
| Denormalise data so it fits one cache line rather than "trampling your cache" (Cook [8]); "Prefetch and cache-align structs" (DE [9]) | 14, 06 |
| Warm the cache: the hot path runs about 0.01% of the time, so run a dummy path through it (Cook [8]) | all (bench note) |
| Measure: p50/p99 histograms per stage (DE [9]); measure end to end in a production-like setup (Cook [8]); perf top-down plus PAPI IPC (Gross [7]) | all |
| Scale: about 2.5 us best wire-to-wire (Cook [8]); under 1 us ultra-low latency, 1-10 us strategy (Gross [7]); p95 under 50 us target (DE [9]) | title cards |
| Zero copy: serialise directly into the queue buffer (Gross [7]) | 06, 16 |

**No source among [7]-[9] covers:** ai-15 fixed-point, ai-16 parsing (beyond zero copy), ai-06 pass-by-value specifically. Paper [6] does support 06 through the missing-move and copy findings. For 15 and 16, cite cppreference or exchange protocol specs, or present them as house practice. Gross's numeric charts (map vs vector, branchless vs linear) did not survive text extraction, so do not quote their results.

## 4. Nuance
None of these sources says general-purpose C++ is wrong. Gross's principles are "Choose the right tool for the right task" and "Understanding your problem (by looking at data!)". Cook stresses that the hot path is a tiny fraction of execution. Startup, config, tooling, and anything off the critical path is fine with std containers, exceptions, and iostream. Paper [6] even finds AI code slightly *better* on correctness and safety, and it found that targeted feedback measurably reduced the inefficiencies. An assistant writes what the prompt asks for. When the prompt states a latency budget, no allocation after startup, bounded sizes, and a single writer, the output changes; then you measure it.

## Links
1. https://www.efinancialcareers.co.uk/news/using-english-as-a-coding-language-won-t-get-you-a-600k-programming-job
2. https://www.newsbytesapp.com/news/science/bjarne-stroustrup-says-ai-generated-code-is-bloated-buggy-insecure/tldr
3. https://www.businesswire.com/news/home/20260806810207/en/
4. https://www.mychesco.com/a/news/regional/susquehanna-adds-c-creator-stroustrup-as-technical-fellow/
5. https://aiweekly.co/alerts/google-study-ai-generated-c-raises-compute-costs-5-8
6. https://arxiv.org/abs/2608.06640 (PDF https://arxiv.org/pdf/2608.06640v1)
7. Gross, CppCon 2024 slides: https://wu-yikun.github.io/documents/cpp/When-Nanoseconds-Matter_Ultrafast-Trading-Systems-in-C++.pdf (overview https://www.optiver.com/insights/technology-blog/designing-low-latency-cpp-systems/, 31 Mar 2025; it lists topics only)
8. Cook, CppCon 2017 slides: https://www.smallake.kr/wp-content/uploads/2023/04/When-a-Microsecond-Is-an-Eternity-Carl-Cook-CppCon-2017.pdf
9. https://deepengineering.substack.com/p/from-nic-to-p99-engineering-low-latency (undated, no author named)
