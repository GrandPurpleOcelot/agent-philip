# Diagram types list
diagram_types = [
    "Let AI decide best Diagram",
    "Class Diagram",
    "Use Case Diagram",
    "Sequence Diagram",
    "Activity Diagram (Flow Chart) - New Syntax",
    "Component Diagram",
    "State Diagram",
    "Object Diagram",
    "Deployment Diagram",
    "Timing Diagram",
    "Interaction Overview Diagram",
    "Wireframe",
    "Archimate Diagram",
    "Gantt Chart",
    "MindMap Diagram",
    "Work Breakdown Structure (WBS) Diagram",
    "JSON Data",
    "YAML Data",
    "EBNF diagram",
    "Network diagram (nwdiag)",
    "Salt (Wireframe)",
    "ArchiMate Diagram",
    "Gantt Chart",
    "MindMap",
    "Maths",
    "Entity Relationship Diagram"
]


diagrams = [
    {
      "diagram_type": "Let AI decide best Diagram",
      "useful_for": "Assistant selects the best fit diagram based on the input requirements.",
      "example": "@startuml\n"
    },
    {
      "diagram_type": "Sequence Diagram",
      "useful_for": "Dynamic modeling of object interactions.",
      "example": "@startuml\nAlice -> Bob: Message\n@enduml"
    },
    {
      "diagram_type": "Activity Diagram (Flow Chart) - New Syntax",
      "useful_for": "Modeling business and software processes.",
      "example": "@startuml\nstart\n:activity;\nstop\n@enduml"
    },
    {
      "diagram_type": "Class Diagram",
      "useful_for": "Software design to show classes and relationships.",
      "example": "@startuml\nClass01 <|-- Class02\n@enduml"
    },
    {
      "diagram_type": "Use Case Diagram",
      "useful_for": "System analysis to represent user interactions.",
      "example": "@startuml\n:User: -- (UseCase)\n@enduml"
    },
    {
      "diagram_type": "Entity Relationship Diagram",
      "useful_for": "Database design to show entity relationships.",
      "example": "@startuml\n[Entity1] -- [Entity2]\n@enduml"
    },
    {
      "diagram_type": "Gantt Chart",
      "useful_for": "Project management to visualize project schedules.",
      "example": "@startgantt\n[Task1] lasts 5 days\n@endgantt"
    },
    {
      "diagram_type": "MindMap Diagram",
      "useful_for": "Brainstorming and organizing thoughts.",
      "example": "@startmindmap\n* MindMap\n** Sub-Topic\n@endmindmap"
    },
    {
      "diagram_type": "Component Diagram",
      "useful_for": "System architecture to show components and dependencies.",
      "example": "@startuml\n[Component1] ..> [Component2]\n@enduml"
    },
    {
      "diagram_type": "State Diagram",
      "useful_for": "Behavioral modeling of state changes.",
      "example": "@startuml\n[*] --> State1\n@enduml"
    },
    {
      "diagram_type": "Deployment Diagram",
      "useful_for": "Planning hardware and software deployment.",
      "example": "@startuml\nnode1 -- node2\n@enduml"
    },
    {
      "diagram_type": "Network diagram (nwdiag)",
      "useful_for": "Designing and visualizing network architectures.",
      "example": "@startnwdiag\nnwdiag {\n  network dmz {\n    web01 [address = '192.168.0.1'];\n  }\n}\n@endnwdiag"
    },
    {
      "diagram_type": "Work Breakdown Structure (WBS) Diagram",
      "useful_for": "Project management to break down projects into manageable parts.",
      "example": "@startwbs\n* Project\n** Task1\n*** Subtask1\n@endwbs"
    },
    {
      "diagram_type": "Object Diagram",
      "useful_for": "Detailed modeling showing instances and relationships.",
      "example": "@startuml\nobject Object1\n@enduml"
    },
    {
      "diagram_type": "Interaction Overview Diagram",
      "useful_for": "Overview of complex system interactions.",
      "example": "@startuml\n(*) --> if \"Condition\" then\n-->[true] \"Activity1\"\n@enduml"
    },
    {
      "diagram_type": "Timing Diagram",
      "useful_for": "Systems engineering to visualize timing constraints.",
      "example": "@startuml\ntiming\n@enduml"
    },
    {
      "diagram_type": "Wireframe",
      "useful_for": "UI/UX design to layout user interfaces.",
      "example": "@startsalt\n{\nJust a simple wireframe\n}\n@endsalt"
    },
    {
      "diagram_type": "JSON Data",
      "useful_for": "Data interchange between systems.",
      "example": "{\n\"key\": \"value\"\n}"
    },
    {
      "diagram_type": "YAML Data",
      "useful_for": "Configuration files and data serialization.",
      "example": "key: value"
    },
    {
      "diagram_type": "EBNF diagram",
      "useful_for": "Specification of computer language syntax.",
      "example": "@startebnf\n\"rule\" = 'definition';\n@endebnf"
    },
    {
      "diagram_type": "ArchiMate Diagram",
      "useful_for": "Enterprise architecture to describe architectures.",
      "example": "@startuml\n[Element] ..> [AnotherElement]\n@enduml"
    },
    {
      "diagram_type": "Salt (Wireframe)",
      "useful_for": "Advanced wireframing.",
      "example": "@startsalt\n{\nYour wireframe here\n}\n@endsalt"
    },
    {
      "diagram_type": "Maths",
      "useful_for": "Mathematical modeling and visualization.",
      "example": "@startmath\n\\sum_{i=1}^n i = \\frac{n(n+1)}{2}\n@endmath"
    }
    ]

sample_plantuml = '''@startuml
participant User
participant "TSLivechat" as TSL
participant "Alice the Chatbot" as Alice
participant "Human Agent" as Agent

User -> TSL: Sends message
TSL -> Alice: Forwards message

alt If escalation is required
    Alice -> User: Notifies about escalation
    Alice -> TSL: Sends escalation signal
    User -> TSL: Sends another message
    TSL -> Agent: Forwards message to human agent
    Agent -> User: Responds to user
    Agent -> TSL: Sends de-escalation signal
else No escalation required
    Alice -> User: Directly responds to query
end

@enduml
'''

sample_plantuml_agent = '''@startuml
skinparam BoxPadding 15
skinparam ParticipantPadding 0
autonumber

title Solution Agent

participant "Client" AS C
participant "Backend" AS B
participant "Decision Engine" AS D
participant "Agent" AS A
participant "Database" AS DB

== Initial Session == 
C -> B: input question
B -> D: get engine by issue question
B --> B: extract jira_ticket, sample_pull_request
B -> DB: store problem in session context
B -> A: generate issue template 
A --> B: generated template
B --> DB: update issue template
B --> C: return issue template

== Q&A Flow ==

C -> B: user send message
B -> D: get next_action and output
D --> D: choose the engine type
note left
There are 2 engine types:
- CommandEngine: if user start message with allowed command: /retrieve, /search, /url, ...
- AgentEngine: if user sent normal message
end note

alt engine is CommandEngine
B --> B: execute command
B -> DB: update repo context if needed
B --> C: show result to user
B -> A: generate new question
A --> B: question
B --> C: send question to user
else engine is AgentEngine
D --> B: next_action and output
B --> B: invoke specific handler base on next_action
note left
next_action:
- Clarification: output has question to user
- Completed: imply that user provided all information to generate issue 
end note

alt next_action is Clarification
B -> A: generate question and suggested answer
A --> B: questions and suggested answer
B --> C: send questions to user
else next_action is Enrich_Issue
B -> A: generate issue base on provided information
A --> B: enriched issue
B --> C: send enriched issue to user
end
end

B -> DB: store messages
@enduml
'''

in_the_beginning = '''Explain the 12 Apostles of Chris and the meaning of their names in a sentence,
and their relationship to Chris.
In the notes describe their stories'''