import os
import json

from crewai import Crew, Agent, Task, Process
# from crewai.project import CrewBase, agent, crew, task

from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import Tool


class BloodReportCrew:
    def __init__(self) -> None:
        self.__groqKey = os.getenv("GROQ_KEY")
        os.environ["GROQ_API_KEY"] = self.__groqKey
        self.groqllm = ChatGroq(
            temperature=0,
            model_name="groq/llama-3.1-70b-versatile",
        )
        self.search_tool = DuckDuckGoSearchRun()
        self.searchllm = Tool(
            name="Web Search",
            func=self.search_tool.run,
            description="Useful for searching the web for current information on health topics.",
        )

    def get_agents(self):
        return [
            Agent(
                role="Medical Data Analyst",
                goal=""" Accurately analyze and interpret blood report data. 
                You analyze and organize the data according to the difference in
                normal value and reorted values, as it is necessary to understand which values might be off the charts.""",
                backstory="""You are an expert in medical data analysis with a focus on blood reports. 
                You do not make up any values and only understands the reports accurately.""",
                allow_delegation=False,
                verbose=True,
                llm=self.groqllm,
            ),
            Agent(
                role="assistant doctor and researcher",
                goal=""" Find and synthesize relevent health information and diagnosis of the data provided from reliable sources.""",
                backstory="""You are a skilled medical researcher with a talent for finding and interpreting the latest health information.""",
                allow_delegation=False,
                verbose=True,
                llm=self.groqllm,
            ),
            Agent(
                role="Patient Communication Specialist",
                goal=""" Translate technical medical information into clear, empathetic patient communications""",
                backstory="""You are a skilled communicator with a talent for translating complex medical information into clear, empathetic patient communications.""",
                allow_delegation=False,
                verbose=True,
                llm=self.groqllm,
            ),
        ]

    def get_tasks(self):
        agents = self.get_agents()
        return [
            Task(
                description=""" Analyze the provided blood report: {report}. Extract and interpret all relevant medical data,
                focusing on test results, reference ranges, and abnormal values.
                Identify key health indicators and potential areas of concern based on the test results""",
                expected_output=""" A structured JSON object containing: Patient information (age, gender, test date),
                Complete list of tests performed, Test results with corresponding units and reference ranges,
                Flagged abnormal results (high or low), Critical values requiring immediate attention.
                Next, A summary report highlighting: Key findings and their potential health implications,
                List of abnormal results ranked by potential severity,
                Suggestions for follow-up tests or areas needing further investigation.""",
                agent=agents[0],
            ),
            Task(
                description=f"""Based on the analysis of the blood report, conduct a comprehensive web search for recent, relevant health-related articles.
                Focus on abnormal test results and their potential health implications.
                Prioritize reputable medical sources and ensure the information is applicable to the patient's demographic.""",
                expected_output="""A synthesized report containing:
                1. Possible health conditions associated with the abnormal results
                2. Potential causes for the abnormalities, including lifestyle factors and medical conditions
                3. General lifestyle or dietary recommendations related to improving the specific test results
                4. Any contradictions or debates found in the medical literature regarding the interpretation of these results
                And, A curated list of references used, including:
                1. Article titles, authors, and publication debates
                2. Source credibility assessment
                3. Brief summaries of key points relevant to the blood test results""",
                agent=agents[1],
            ),
            Task(
                description=f""" Transform the technical analysis and web search results into a clear, empathetic, and accessible email communication.
                The email should inform the patient about their test results in a way that is easy to understand, sensitive to potential concerns,and encourages appropriate follow-up actions.
                Maintain a caring and supportive tone throughout the communication.""",
                expected_output=""" An email draft that includes:
                1. A warm and personalized greeting
                2. A clear, non-technical summary of the blood test results, highlighting: Normal results to provide reassurance,
                    Abnormal results explained in simple terms, avoiding alarmist language,
                    Potential implications of abnormal results, presented factually but sensitively
                3. General lifestyle recommendations related to the test results, framed positively as opportunities for health improvement
                4. Encouragement to discuss the results with a healthcare provider, including: Suggested questions to ask during the follow-up,
                    Emphasis on the importance of professional medical advice.
                5. A compassionate closing that offers support and encourages the patient to reach out with any questions or concerns.
                The email should use plain language, avoid medical jargon where possible,
                and maintain a balance between being informative and being sensitive to the patient's potential emotional response to their test results.""",
                agent=agents[2],
            ),
        ]

    def get_crew(self):
        return Crew(
            agents=self.get_agents(),
            tasks=self.get_tasks(),
            processes=Process.sequential,
            verbose=True,
        )

    def kickoff(self, report):
        crew = self.get_crew()
        result = crew.kickoff(inputs={"report": report})

        return result


# @CrewBase
# class BloodReportCrew:
#     """
#     Blood Report Crew (Analyse Blood Report)
#     """
#
#     agents_config = "./config/agents.yaml"
#     tasks_config = "./config/tasks.yaml"
#
#     def __init__(self) -> None:
#         # self.pdf_reader_tool = PDFAnalyzer()
#         self.__groqKey = os.getenv("GROQ_KEY")
#         os.environ["GROQ_API_KEY"] = self.__groqKey
#         self.groqllm = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768")
#         self.search_tool = DuckDuckGoSearchRun()
#         self.searchllm = Tool(
#             name="Web Search",
#             func=self.search_tool.run,
#             description="Useful for searching the web for current information on health topics.",
#         )
#         print("Blood Report Crew Initialized!!!")
#
#     @agent
#     def report_analyzer(self):
#         """
#         Analyze Blood Report
#         """
#         print("Report Analyzer")
#         return Agent(
#             config=self.agents_config["report_analyzer"],
#             tools=self.groqllm,
#         )
#
#     @agent
#     def assistant_doctor(self):
#         """
#         Web Search
#         """
#         print("Assistant Doctor")
#         return Agent(
#             config=self.agents_config["assistant_doctor"],
#             tool=self.searchllm,
#         )
#
#     @agent
#     def communication_specialist(self):
#         """
#         writer
#         """
#         print("Communication Specialist")
#         return Agent(
#             config=self.agents_config["communication_specialist"],
#             tool=self.groqllm,
#         )
#
#     @task
#     def analyze_report(self):
#         """
#         Analyze Blood Report
#         """
#         return Task(
#             config=self.tasks_config["blood_report_analysis"],
#             agent=self.report_analyzer,
#         )
#
#     @task
#     def search(self):
#         """
#         Web Search
#         """
#         return Task(
#             config=self.tasks_config["web_search"],
#             agent=self.assistant_doctor,
#         )
#
#     @task
#     def email_writing(self):
#         """
#         email writing
#         """
#         return Task(
#             config=self.tasks_config["communication_result"],
#             agent=self.communication_specialist,
#         )
#
#     @crew
#     def blood_report_crew(self) -> Crew:
#         return Crew(
#             agents=self.agents,
#             tasks=self.tasks,
#             processes=Process.sequential,
#             verbose=2,
#         )
#
#
# async def bloodcrew(inp):
#     br = BloodReportCrew()
#     result = await br.crew.kickoff_async(inputs=inp)
#     return result
