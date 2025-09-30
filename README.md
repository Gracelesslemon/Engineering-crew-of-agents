# Engineering Crew: AI-Powered Software Development Team

A CrewAI project that orchestrates a team of specialized AI agents to collaboratively design, implement, and test software applications.

## Overview

This project demonstrates autonomous software development using CrewAI's multi-agent framework. Four specialized agents work together to transform high-level requirements into an application.

## Agent Architecture

All agent and task configurations are defined as YAML files in the `config/` folder for easy customization.

### Engineering Lead
Translates high-level requirements into detailed technical specifications and system designs for the development team.

### Backend Engineer
Implements Python modules based on the engineering lead's specifications. Executes code safely within isolated Docker containers to ensure system security.

### Frontend Engineer
Builds interactive Gradio user interfaces according to design specifications, creating intuitive interfaces for end users.

### Test Engineer
Develops comprehensive unit tests to validate functionality and ensure code quality.

## Tech Stack

- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **AI Framework**: [CrewAI](https://www.crewai.com/)
- **LLM**: Gemini 2.0
- **UI Framework**: [Gradio](https://www.gradio.app/)
- **Containerization**: Docker

## Screenshots:
> [!NOTE]
> No directions were given stating how the ui should look.
### Account Actions page:
<img width="1918" height="907" alt="image" src="https://github.com/user-attachments/assets/af860cfe-0021-4500-b7d6-d6ef3f626214" />

### Trade page:
<img width="1916" height="911" alt="image" src="https://github.com/user-attachments/assets/e7eea6d6-fa84-4745-9b73-6a7b36feb525" />

### Reports page:
<img width="1916" height="913" alt="image" src="https://github.com/user-attachments/assets/094e7bbf-d4ac-434c-9960-a88c4d693a24" />


## Current Limitations

- **Code Formatting**: Despite explicit instructions to avoid markdown formatting, Gemini 2.0 occasionally wraps code in backticks, requiring manual cleanup
- **Test Completeness**: Generated unit tests sometimes miss boilerplate code like:
```python
  if __name__ == "__main__":
      unittest.main()
```
- Other minor issues exist, but they can be easily addressed with sufficient LLM API resources and prompt optimization.
