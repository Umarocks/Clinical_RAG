# 🧠 AI-Powered Clinical Documentation & Coding Assistant Bot

An AI-based assistant designed to simplify and accelerate clinical documentation and coding workflows using **Retrieval-Augmented Generation (RAG)**. Ask natural-language questions related to clinical documentation, diagnosis codes, or compliance — and get precise answers backed by source references and medical documentation visuals.


![Demo](https://files.catbox.moe/5na67n.png)


---

## 🚀 Features

- **🔍 Ask Clinical Documentation & Coding Questions**  
  Whether you're unsure about how to document a condition or what diagnosis code applies — just ask.  

- **🤖 RAG-Based AI Responses**  
  Combines the power of Large Language Models (LLMs) with real-time retrieval of relevant data from trusted reference sources like CDI manuals, ICD-10/CPT guides, and CMS documentation.

- **📚 Source-Linked Answers**  
  Every AI response includes:
  - 📄 Exact matching source text  
  - 📘 Reference book or documentation guide  
  - 🖼️ Relevant image snippets (when available)



https://github.com/user-attachments/assets/24cc8f2d-7753-46dd-839f-b5230be5f684



- **⏱️ Speeds Up Documentation & Coding**  
  - Physicians can ensure complete and compliant clinical notes.  
  - Coders can clarify vague documentation and retrieve coding guidelines faster.  
  - CDIS teams can improve accuracy and reduce queries.


![Demo](https://files.catbox.moe/c36h89.png)


---

## 💼 Use Cases

- **Physicians**: Ensure compliant EHR documentation.  
- **Medical Coders**: Get quick access to coding rules and clarifications.  
- **CDI Specialists**: Validate documentation quality and stay up-to-date.  
- **Students**: Learn proper documentation and coding with source-backed AI support.

---

## 🧰 Tech Stack

- **LLM Integration**: OpenAI 
- **RAG Pipeline**: LangChain 
- **Document Store**: FAISS 
- **Backend**: Python, Flask  
- **OCR & PDF Parsing**: Tesseract, PyMuPDF , Docling 
- **Frontend**: React 

---

## 🗂️ How It Works

1. **User Asks a Question**  
   Example: _"What documentation is required for coding acute respiratory failure?"_

2. **RAG Fetches Contextual Information**  
   Pulls relevant chunks from official coding guidelines, documentation manuals, and reference texts.

3. **LLM Generates a Response**  
   Combines retrieved info with AI reasoning to generate a high-quality answer.

4. **Output is Presented**  
   - ✅ Clean, concise answer  
   - 🔗 Reference text with metadata  
   - 🖼️ Image snippet from source (if available)
  

![Demo](https://files.catbox.moe/n4u14w.png)


---

## 📖 References Used

- ICD-10-CM and ICD-10-PCS Guidelines  
- CPT 2024 Professional Edition  
- *More guides can be added as per requirement*

---

## 📦 Deployment

- Run locally with Docker  
- Cloud deployment supported (AWS/GCP/Azure)  
- Option for on-prem HIPAA-compliant setup  
- API integration possible for EHRs (e.g., Epic, Cerner)

---

## 🛣️ Roadmap

- ✅ RAG integration with clinical datasets  
- ✅ Source-based image display  
- 🛠️ Speech-to-text for voice-based inputs  
- 🛠️ Auto-document generation for clinical scenarios  
- 🛠️ Smart alerts for insufficient documentation  
- 🛠️ EHR integration modules

---

## 🤝 Contributing

We welcome developers, clinicians, data scientists, and health IT professionals!  
Feel free to fork this repo, raise issues, or submit pull requests.

---

## 📬 Contact

For demos, feature requests, or collaboration:  
📧 **Email:** umar.a.aziz2001@gmail.com 
🌐 **Github:** [Github](https://github.com/Umarocks)]  
📘 **LinkedIn:** [LinkedIn](https://linkedin.com/in/umarocks/)]

---

> ⚠️ Disclaimer: This tool is intended to assist professionals and should not be solely relied on for clinical decisions. Always verify with official sources.
