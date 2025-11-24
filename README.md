**HERE'S FOR THE WIN AND ALWAYS THE WIN!**
schleiden-virtual-robot/
│── main.py               → Launch the entire robot
│── requirements.txt       → Libraries needed
│
├── analyzer/
│   ├── analyzer.py        → NLP logic & command routing
│   └── database.yaml      → FAQ + learned knowledge
│
├── robot/
│   ├── brain.py           → Central controller
│   ├── eyes.py            → Image-render + blinking
│   ├── speech.py          → TTS
│   ├── stt.py             → Speech recognition
│   └── camera_detector.py → Face detection logic
│
├── ui/
│   └── main_window.py     → GUI window
│
├── assets/
│   └── expressions/       → PNG expression frames
│
└── data/
    └── faq_schleiden.yaml → Predefined knowledge base
