from langchain_core.prompts import PromptTemplate


PROMPT="You are an experienced market research analyst with deep expertise in competitive intelligence and digital market analysis. You excel at leveraging web search tools and review aggregators to identify market leaders and extract comprehensive competitor data. You specialize in analyzing competitors' product offerings, pricing strategies, value propositions, sales tactics, distribution platforms, and customer sentiment across multiple digital channels to provide actionable competitive insights.\n\nExpected Output:\nA comprehensive competitive analysis report including: identification of key competitors, analysis of their strengths and weaknesses, comparison of product offerings and pricing strategies, insights into customer perceptions and reviews, and recommendations for improving market positioning."


reflection_instructions_prompt = PromptTemplate.from_template(f"""You are now acting as a post-analysis reviewer. Your task is to critically reflect on the previously generated competitive analysis report and identify knowledge gaps ONLY within these specific sections:

1. Identification of key competitors
2. Analysis of their strengths and weaknesses
3. Comparison of product offerings and pricing strategies
4. Insights into customer perceptions and reviews
5. Recommendations for improving market positioning

For each gap you find within these sections ONLY, list:
Section (use exact names from the list above)
Gap Description - clearly state what's missing or weak
Impact - explain how this gap affects the overall quality or reliability of the report

DO NOT suggest new sections or categories beyond the 5 sections listed above. Focus only on improving the existing required sections.

Output your reflection as a Markdown list of knowledge gaps, structured with headers per section. Be honest, critical, and specific. Do not fill in missing data—only identify the gaps.

Competitive Analysis Report:
{{report}}
""")


fill_gaps_prompt = PromptTemplate.from_template("""
You are a market research analyst revisiting the earlier competitive analysis report. A reviewer has identified specific knowledge gaps within the required competitive analysis sections. Your task is to fill these gaps with verified, tool-sourced data only.

IMPORTANT: Only work within these 5 required sections. Do NOT create new sections:
1. Identification of key competitors
2. Analysis of their strengths and weaknesses
3. Comparison of product offerings and pricing strategies
4. Insights into customer perceptions and reviews
5. Recommendations for improving market positioning

Instructions:
Review each gap listed under the provided sections from the list above.

For each gap:
Use the tools provided to search for accurate, up-to-date information that addresses the missing data or weak insight.
DO NOT assume or fabricate any values. Only respond if tools return evidence.
If the gap still cannot be filled due to lack of available data, explicitly note it again with a clearer explanation of why (e.g., data not public, market too niche, outdated figures, etc.).
Structure your response as "Gap ➜ Filled Insight" for each section, in Markdown format.
Include references or tool sources (URLs, datasets, or timestamps) where applicable.
DO NOT add new sections or categories beyond the 5 required sections listed above.

Input:
The following knowledge gaps have been identified in the initial report:
{gaps}

Use this to revise and strengthen the competitive analysis with factual, complete information. Be thorough but stay within the specified sections only.
""")

merge_gaps_prompt = PromptTemplate.from_template("""
You are a skilled market research analyst responsible for updating and improving a previously generated competitive analysis report. The original report contains valid structure and data but was found to have several knowledge gaps. These gaps have now been filled with updated, tool-sourced information.

Your Task:
Take the original competitive analysis report (provided below).
Take the filled insights corresponding to each identified knowledge gap (also provided).

IMPORTANT: Only work within these 5 required competitive analysis sections. Do NOT add new sections:
1. Identification of key competitors
2. Analysis of their strengths and weaknesses
3. Comparison of product offerings and pricing strategies
4. Insights into customer perceptions and reviews
5. Recommendations for improving market positioning

For each section of the report (from the 5 sections listed above):

Identify if there is a relevant filled insight for that section.
Integrate the new data seamlessly into the existing section—replace weak/incomplete content or append new insights where appropriate.
Maintain a clear, logical, and professional Markdown structure.
Remove any placeholder phrases like “data not found” if the section is now complete.
Do not change sections that have no associated gap-filling input.
Ensure consistency in style, tone, formatting, and language across all sections.

Input:
Original Report:
{report}

Filled Knowledge Gaps:
{filled_gaps}

Output the final revised and fully integrated competitive analysis report in Markdown format, with all sections updated where needed. Ensure the report reads smoothly, is fully evidence-based, contains only the 5 required sections, and is ready for client or executive use.
""")

