// Made by tutorial.py, don't edit by hand
const LESSONS = [
 {
  "title": "Honest cats tell the truth",
  "intro": "Ash is honest: the \ud83d\udd12 in the corner of Ash's card means it's given. So Ash's clue is true. Tap Bean to mark it: once for honest, twice for liar.",
  "why": {
   "1": "Ash is honest, so Ash's clue is true: Bean is a liar."
  },
  "done": "Right! And Bean's clue is false, just like a liar's clue should be.",
  "puzzle": {
   "rows": 1,
   "cols": 2,
   "seed": null,
   "level": "lesson",
   "given": 0,
   "cats": [
    {
     "name": "Ash",
     "color": "orange",
     "row": 0,
     "column": 0,
     "text": "Bean is a liar.",
     "hidden": false,
     "secret": null,
     "mentions": [
      1
     ],
     "mood": "angry",
     "clue": {
      "cats": [
       0,
       1
      ],
      "table": "Bg=="
     }
    },
    {
     "name": "Bean",
     "color": "black",
     "row": 0,
     "column": 1,
     "text": "Ash is a liar.",
     "hidden": false,
     "secret": null,
     "mentions": [
      0
     ],
     "mood": "angry",
     "clue": {
      "cats": [
       0,
       1
      ],
      "table": "Bg=="
     }
    }
   ],
   "liars": [
    false,
    true
   ]
  }
 },
 {
  "title": "Liars never tell the truth",
  "intro": "Nothing is given this time. Try both options for Ash: could Ash be honest?",
  "why": {
   "0": "If Ash were honest, Ash's clue would be true, and then Ash would be a liar. So Ash is a liar.",
   "1": "Ash is a liar, so Ash's clue is false: at least one of them is honest. That's Bean."
  },
  "after": {
   "1": [
    0
   ]
  },
  "next": {
   "1": "Right, Ash is a liar! So Ash's clue is false. What does that tell you about Bean?"
  },
  "done": "That's the whole trick: a liar's clue is always false.",
  "puzzle": {
   "rows": 1,
   "cols": 2,
   "seed": null,
   "level": "lesson",
   "given": null,
   "cats": [
    {
     "name": "Ash",
     "color": "white",
     "row": 0,
     "column": 0,
     "text": "Bean and I are both liars.",
     "hidden": false,
     "secret": null,
     "mentions": [
      1
     ],
     "mood": "angry",
     "clue": {
      "cats": [
       0,
       1
      ],
      "table": "Ag=="
     }
    },
    {
     "name": "Bean",
     "color": "grey",
     "row": 0,
     "column": 1,
     "text": "Ash is a liar.",
     "hidden": false,
     "secret": null,
     "mentions": [
      0
     ],
     "mood": "angry",
     "clue": {
      "cats": [
       0,
       1
      ],
      "table": "Bg=="
     }
    }
   ],
   "liars": [
    true,
    false
   ]
  }
 },
 {
  "title": "One cat leads to the next",
  "intro": "Solve one cat, then use its clue to solve the next. A liar's clue is false, so flip it.",
  "why": {
   "1": "Ash is honest, so Bean is a liar.",
   "2": "Bean is a liar, so Bean's clue is false: Cleo is a liar too."
  },
  "after": {
   "2": [
    1
   ]
  },
  "next": {
   "2": "Right, Bean is a liar! So flip Bean's clue. What does it tell you about Cleo?"
  },
  "done": "That's chaining: every cat you solve tells you how to read its clue.",
  "puzzle": {
   "rows": 1,
   "cols": 3,
   "seed": null,
   "level": "lesson",
   "given": 0,
   "cats": [
    {
     "name": "Ash",
     "color": "yellow",
     "row": 0,
     "column": 0,
     "text": "Bean is a liar.",
     "hidden": false,
     "secret": null,
     "mentions": [
      1
     ],
     "mood": "angry",
     "clue": {
      "cats": [
       0,
       1
      ],
      "table": "Bg=="
     }
    },
    {
     "name": "Bean",
     "color": "brown",
     "row": 0,
     "column": 1,
     "text": "Cleo is honest.",
     "hidden": false,
     "secret": null,
     "mentions": [
      2
     ],
     "mood": "happy",
     "clue": {
      "cats": [
       1,
       2
      ],
      "table": "CQ=="
     }
    },
    {
     "name": "Cleo",
     "color": "orange",
     "row": 0,
     "column": 2,
     "text": "Ash is a liar.",
     "hidden": false,
     "secret": null,
     "mentions": [
      0
     ],
     "mood": "angry",
     "clue": {
      "cats": [
       0,
       2
      ],
      "table": "Bg=="
     }
    }
   ],
   "liars": [
    false,
    true,
    true
   ]
  }
 },
 {
  "title": "Your tools",
  "intro": "A tiny puzzle to try the buttons on. I'll show you each one.",
  "tour": [
   {
    "id": "note",
    "point": "pen",
    "cat": 3,
    "done": {
     "note": 3
    },
    "text": "Doodle is honest, so its clue is true. Tap \u270e on Doodle and write that down in your own words. You can add a tag there too.",
    "placeholder": "e.g. one of Biscuit and Clover is a liar"
   },
   {
    "id": "connections",
    "point": "card",
    "cat": 3,
    "done": {
     "connections": 3
    },
    "text": "{press} Doodle to see which cats talk about Doodle."
   },
   {
    "id": "clover",
    "point": "card",
    "cat": 2,
    "done": {
     "mark": [
      2,
      "honest"
     ]
    },
    "text": "Clover talks about Doodle: \"Doodle is honest.\" That's true, so Clover is honest too. Mark Clover."
   },
   {
    "id": "hint",
    "point": "hint",
    "done": {
     "mark": [
      1,
      "liar"
     ]
    },
    "text": "Who's next? Press Hint to see a clue that works right now.",
    "again": "That's Doodle's clue. Press Hint again to see which cat it finds.",
    "found": "Doodle's clue finds Biscuit: one of Biscuit, Clover and Doodle is a liar, and it's not Clover or Doodle. Mark Biscuit."
   },
   {
    "id": "used",
    "point": "check",
    "cat": 3,
    "done": {
     "used": 3
    },
    "text": "Doodle's clue is used up. Tap its \u2713 to grey it out. Clover's and Biscuit's are used up too, grey them out if you like."
   },
   {
    "id": "last",
    "text": "Figure out Apricot yourself now!"
   }
  ],
  "why": {
   "0": "Biscuit is a liar, so Doodle is the only honest cat in column 2. Apricot's clue is true: Apricot is honest.",
   "1": "Doodle is honest, so exactly one of Biscuit, Clover and Doodle is a liar. That's Biscuit.",
   "2": "If Clover were a liar, Clover's clue would be false, and Doodle would be a liar. But Doodle is honest."
  },
  "after": {
   "0": [
    1
   ],
   "1": [
    2
   ]
  },
  "done": "Solved! Those tools are there in every puzzle, use them whenever they help.",
  "puzzle": {
   "rows": 2,
   "cols": 2,
   "seed": 400,
   "level": "lesson",
   "given": 3,
   "cats": [
    {
     "name": "Apricot",
     "color": "orange",
     "row": 0,
     "column": 0,
     "text": "Doodle is the only honest cat among the cats in column 2.",
     "hidden": false,
     "secret": null,
     "mentions": [
      1,
      3
     ],
     "mood": "neutral",
     "clue": {
      "cats": [
       0,
       1,
       3
      ],
      "table": "pg=="
     }
    },
    {
     "name": "Biscuit",
     "color": "white",
     "row": 0,
     "column": 1,
     "text": "Clover and I are both honest.",
     "hidden": false,
     "secret": null,
     "mentions": [
      2
     ],
     "mood": "happy",
     "clue": {
      "cats": [
       1,
       2
      ],
      "table": "Cw=="
     }
    },
    {
     "name": "Clover",
     "color": "orange",
     "row": 1,
     "column": 0,
     "text": "Doodle is honest, fur real.",
     "hidden": false,
     "secret": null,
     "mentions": [
      3
     ],
     "mood": "happy",
     "clue": {
      "cats": [
       2,
       3
      ],
      "table": "CQ=="
     }
    },
    {
     "name": "Doodle",
     "color": "white",
     "row": 1,
     "column": 1,
     "text": "Exactly one of Biscuit, Clover and me is a liar.",
     "hidden": false,
     "secret": null,
     "mentions": [
      1,
      2
     ],
     "mood": "neutral",
     "clue": {
      "cats": [
       1,
       2,
       3
      ],
      "table": "5g=="
     }
    }
   ],
   "liars": [
    false,
    true,
    false,
    false
   ]
  }
 },
 {
  "title": "Your turn",
  "intro": "A real puzzle. At every step exactly one clue helps. Stuck? Press Next step.",
  "steps": [
   {
    "speaker": 3,
    "cat": 4,
    "text": "Read Felix's clue. Then Honey must be honest."
   },
   {
    "speaker": 4,
    "cat": 1,
    "text": "Read Honey's clue. Then Dusty must be honest."
   },
   {
    "speaker": 1,
    "cat": 6,
    "text": "Read Dusty's clue. Then Mochi must be a liar."
   },
   {
    "speaker": 6,
    "cat": 0,
    "text": "Read Mochi's clue. Then Cricket must be honest."
   },
   {
    "speaker": 0,
    "cat": 8,
    "text": "Read Cricket's clue. Then Otis must be a liar."
   },
   {
    "speaker": 8,
    "cat": 7,
    "text": "Read Otis's clue. Then Nimbus must be honest."
   },
   {
    "speaker": 5,
    "cat": 2,
    "text": "Read Juniper's clue. Then Espresso must be a liar."
   },
   {
    "speaker": 7,
    "cat": 5,
    "text": "Read Nimbus's clue. Then Juniper must be honest."
   }
  ],
  "done": "You solved a whole puzzle! Pick a level in the menu to keep going.",
  "puzzle": {
   "rows": 3,
   "cols": 3,
   "seed": 1434,
   "level": "lesson",
   "given": 3,
   "cats": [
    {
     "name": "Cricket",
     "color": "brown",
     "row": 0,
     "column": 0,
     "text": "Exactly 2 of Nimbus's neighbors are liars.",
     "hidden": false,
     "secret": null,
     "mentions": [
      4,
      6,
      8
     ],
     "mood": "neutral",
     "clue": {
      "cats": [
       0,
       4,
       6,
       8
      ],
      "table": "apY="
     }
    },
    {
     "name": "Dusty",
     "color": "yellow",
     "row": 0,
     "column": 1,
     "text": "Felix is honest, but Mochi is a liar.",
     "hidden": false,
     "secret": null,
     "mentions": [
      3,
      6
     ],
     "mood": "neutral",
     "clue": {
      "cats": [
       1,
       3,
       6
      ],
      "table": "mg=="
     }
    },
    {
     "name": "Espresso",
     "color": "orange",
     "row": 0,
     "column": 2,
     "text": "I'm the only honest cat among Juniper, Otis and me.",
     "hidden": false,
     "secret": null,
     "mentions": [
      5,
      8
     ],
     "mood": "neutral",
     "clue": {
      "cats": [
       2,
       5,
       8
      ],
      "table": "6g=="
     }
    },
    {
     "name": "Felix",
     "color": "brown",
     "row": 1,
     "column": 0,
     "text": "Honey is honest, fur real.",
     "hidden": false,
     "secret": null,
     "mentions": [
      4
     ],
     "mood": "happy",
     "clue": {
      "cats": [
       3,
       4
      ],
      "table": "CQ=="
     }
    },
    {
     "name": "Honey",
     "color": "brown",
     "row": 1,
     "column": 1,
     "text": "Dusty is honest, fur real.",
     "hidden": false,
     "secret": null,
     "mentions": [
      1
     ],
     "mood": "happy",
     "clue": {
      "cats": [
       1,
       4
      ],
      "table": "CQ=="
     }
    },
    {
     "name": "Juniper",
     "color": "yellow",
     "row": 1,
     "column": 2,
     "text": "Exactly 3 of the cats on the edges are liars. Meow.",
     "hidden": false,
     "secret": null,
     "mentions": [
      0,
      1,
      2,
      3,
      6,
      7,
      8
     ],
     "mood": "neutral",
     "clue": {
      "cats": [
       0,
       1,
       2,
       3,
       5,
       6,
       7,
       8
      ],
      "table": "gGiX6WgW6f5oFun+FgH+/2gW6f4WAf7/FgH+/wEA//8="
     }
    },
    {
     "name": "Mochi",
     "color": "yellow",
     "row": 2,
     "column": 0,
     "text": "Felix is the only honest cat among the cats above me.",
     "hidden": false,
     "secret": null,
     "mentions": [
      0,
      3
     ],
     "mood": "neutral",
     "clue": {
      "cats": [
       0,
       3,
       6
      ],
      "table": "0g=="
     }
    },
    {
     "name": "Nimbus",
     "color": "orange",
     "row": 2,
     "column": 1,
     "text": "There are exactly 3 liars in total.",
     "hidden": false,
     "secret": null,
     "mentions": [
      0,
      1,
      2,
      3,
      4,
      5,
      6,
      8
     ],
     "mood": "neutral",
     "clue": {
      "cats": [
       0,
       1,
       2,
       3,
       4,
       5,
       6,
       7,
       8
      ],
      "table": "gGhoFmgWFgFoFhYBFgEBAJfp6f7p/v7/6f7+//7///9oFhYBFgEBABYBAQABAAAA6f7+//7////+/////////w=="
     }
    },
    {
     "name": "Otis",
     "color": "yellow",
     "row": 2,
     "column": 2,
     "text": "Mochi and Nimbus are both honest, or both liars.",
     "hidden": false,
     "secret": null,
     "mentions": [
      6,
      7
     ],
     "mood": "neutral",
     "clue": {
      "cats": [
       6,
       7,
       8
      ],
      "table": "aQ=="
     }
    }
   ],
   "liars": [
    false,
    false,
    true,
    false,
    false,
    false,
    true,
    false,
    true
   ]
  }
 }
];
