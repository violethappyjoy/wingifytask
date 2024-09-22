**ReadMe for Wingify Software Pvt. Ltd. Task**<br>
*Author: Divyanshu Bhardwaj*

# How to run the code
Step1: Steup `.env` file according to `.env.example` file and as necessary.<br>
Step2: With cwd as cloned folder, run `docker-compose up -d --build` to start the servicess.<br>
Step3: Frontend will be available at `http://localhost:5173/` and API Documentation at `http://0.0.0.0:8100`(can use localhost as well).<br>
Step4: Need to add user using `Sign Up` to test.<br>

# My Approach
1. Workflow is divided into 3 parts: Frontend, Backend and Database.<br>
   1.1 Frontend: Simple `vue` template.<br>
   1.2 Backend: `fast-api` is used for backend logic.<br>
   1.3 Database: `postgresql` is used for storing user data.<br>
2. Intution behind parsing the blood report is to extract the data and create a pipeline of crewAI agents.<br>
3. The pipeline followed is: **Understanding Report, What is in there and organize it in terms of what requires attention**-> **Synthesize the problems in the report, what can cause harm and find material on the internet for the same**-> **Create a non-jargon mail to address the report to the end user.**
  *To get links, DuckDuckGo llm can we switched instead of Groq/LLama*<br>
4. Lastly, the report is sent to the user via mail.<br>
5. For security, JWT(in header) is used for authentication and password is hashed before storing in database.<br>
6. A sample report is attached in the codebase for testing. Also, a sample mail output screenshot is attached(without links).
