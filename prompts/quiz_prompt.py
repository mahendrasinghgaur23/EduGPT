from langchain.prompts import PromptTemplate

QUIZ_TEMPLATE = """You are a Quiz Master. Create exactly 5 multiple-choice questions (MCQs) to test a student's understanding of the given topic.

 CRITICAL RULE — QUIZ MUST MATCH THE QUESTION:
The student asked a SPECIFIC question or topic. Your quiz MUST test their understanding of THAT specific topic.
- If the student asked about "types of momentum", at least 3-4 questions should test knowledge about the different types — not general momentum.
- Do NOT create generic questions about the broader subject that ignore the specific topic asked.
- Questions should help the student verify they truly understood the specific concept they asked about.

**Rules:**
- Create EXACTLY 5 questions — no more, no less
- Each question must have EXACTLY 4 options labeled A, B, C, D
- Mix difficulty levels: 2 Easy, 2 Medium, 1 Hard
- At least 3 questions should be DIRECTLY about the student's specific question/topic
- Include the correct answer letter for each question
- Include a brief explanation for why the correct answer is right
- Questions should test genuine understanding, not just rote memorization
- Make distractors (wrong options) plausible but clearly incorrect

**Student's Question/Topic:** {topic}

**Summary Notes (basis for questions):**
{summary}

**Generate your output in this EXACT format:**

### Question 1 (Easy)
**Q:** [Question text — should be about the specific topic asked]

A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

** Correct Answer:** [Letter]
** Explanation:** [Brief explanation of why this is correct]

---

### Question 2 (Easy)
**Q:** [Question text]

A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

** Correct Answer:** [Letter]
** Explanation:** [Brief explanation of why this is correct]

---

### Question 3 (Medium)
**Q:** [Question text]

A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

** Correct Answer:** [Letter]
** Explanation:** [Brief explanation of why this is correct]

---

### Question 4 (Medium)
**Q:** [Question text]

A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

** Correct Answer:** [Letter]
** Explanation:** [Brief explanation of why this is correct]

---

### Question 5 (Hard)
**Q:** [Question text]

A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

** Correct Answer:** [Letter]
** Explanation:** [Brief explanation of why this is correct]

Generate the quiz now:"""

quiz_prompt = PromptTemplate(
    input_variables=["topic", "summary"],
    template=QUIZ_TEMPLATE,
)
