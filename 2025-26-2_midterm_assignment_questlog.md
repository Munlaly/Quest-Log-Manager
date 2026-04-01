# Mid-Term Assignment: QuestLog

## Overview & Goal

This project is a comprehensive command-line application that serves as an adventure quest and inventory assistant. It combines interactive commands with batch file processing to manage a quest log and the player's inventory. The goal is to build a robust, object-oriented application that demonstrates your mastery of all concepts covered in the course so far, from data structures and OOP to error handling and file management.

The application will operate in two modes:

1. **Single Command Mode (Default):** When run with a command (e.g., `python main.py plan`), it executes the task and immediately exits.
2. **Interactive Mode:** When run with the special `manage` command (`python main.py manage`), it enters a continuous command-line session for managing the inventory and quests.

The core of this application involves several key algorithms: a **Planning Analysis** to find completable quests, a **Gap Analysis** to list missing items for a quest, and a **Quest Completion** flow to consume items from the inventory.

## Core Concepts Covered

- **Object-Oriented Programming:** Designing and using classes to model real-world concepts and encapsulate data and behavior.
- **Command-Line Interaction:** Parsing system arguments (`sys.argv`) to control application flow.
- **Data Structures:** Using lists and dictionaries effectively to manage collections of quests and inventory items.
- **File Management:** Reading from and writing to multiple files using `with open()`, including a configuration file, data files and reporting.
- **Data Persistence:** Using the `json` module to serialize and deserialize complex Python objects into files.
- **Error Handling:** Building a resilient application using `try...except` blocks to handle file errors, invalid user input, and other errors.

---

## Detailed Functional Requirements

### 1. Execution Modes

- **Requirement:** The application must inspect command-line arguments to determine its mode of operation.
- **Acceptance Criteria:**
  - If the script is run with `manage` as the first argument, it enters an interactive loop with a command prompt (e.g., `>`) and process user commands. The main loop should be case-insensitive and ignore leading/trailing whitespace.
  - If the script is run with any other command and its arguments, it executes that single command and then terminates.

### 2. Configuration Loading

- **Requirement:** At startup, the application must read a `config.json` file to get the file paths for the quest log and inventory data.
- **Acceptance Criteria:** The application uses the paths specified in the config file for all file operations.

### 3. Supported Commands

The application must support the following command structure.

- **Application Mode:**
  - `manage`: Enters the interactive command loop.

- **Quest Commands:**
  - `quest list`: Prints a simple, numbered list of all available quest names.
  - `quest view "<quest_name>"`: Prints the full details of a specific quest, including its name and list of required items.
  - `quest gap "<quest_name>"`: Performs a "gap analysis" and prints a list of missing items (and quantities) needed to complete that quest.
  - `quest complete "<quest_name>"`: Checks if a quest is completable. If it is, it consumes the required items from the inventory. If not, it reports an error.

- **Inventory Commands:**
  - `inventory add "<item_name>" <quantity>`: Adds the specified quantity to an item in the inventory. If the item doesn't exist, it should be added. The quantity should be an integer.
  - `inventory use "<item_name>" <quantity>`: Reduces the quantity of an item. Must fail with an error if stock is insufficient.
  - `inventory process <filepath>`: Reads a text file where each line is a command (e.g., `ADD potion 5`) and executes them sequentially.

- **Analysis Command:**
  - `plan`: Analyzes the current inventory and prints a list of all "completable" quests.

- **Interactive-Only Command:**
  - `exit`: Saves the final state of the inventory and terminates the interactive session.

### 4. Data Persistence

- **Requirement:** The inventory data file must be automatically updated and saved after any command that modifies its state (`inventory add`, `inventory use`, `inventory process`, `quest complete`).
- **Acceptance Criteria:** `inventory.json` always reflects the latest inventory.

### 5. Report Generation

- **Requirement:** The process command must generate a report file.
- **Acceptance Criteria:** `report.txt` is generated after a process command, logging the outcome of each line.

### 6. Error Handling

- **Requirement:** The application must not crash and must provide user-friendly error messages.
- **Acceptance Criteria:** Handles `FileNotFoundError`, `ValueError` for quantities, invalid commands, incorrect arguments, and logical errors (e.g., using an item that isn't in the inventory, completing a quest with insufficient items).

---

## Implementation Tips & Guidance

### 1. Project Structure

A good project structure will make your life easier. Consider organizing your files in a way that separates data, reports, and your main application logic.

```
/questlog_project
|-- main.py              # Main script to run the application
|-- /questlog            # directory for the questlog package python files
….                       # python files
|-- config.json          # Configuration for file paths
|-- /data
|   |-- quests.json      # Your quest log data
|   |-- inventory.json   # Your inventory data
|-- /reports
|-- report.txt           # Output for the 'process' command
```

### 2. Object-Oriented Design

Think about the main components of your application and how they can be represented as classes.

- **Quest Class:** This class should be responsible for holding the information about a single quest, such as its name and its required items (with quantities).
- **Inventory Class:** This class should manage the inventory of items. It should handle the logic for adding, using, and checking the availability of items.
- **QuestLogManager Class (The Engine):** This class should act as the central controller of your application. It will orchestrate the interactions between the quests and the inventory, load and save data, and contain the logic for executing user commands.

### 3. Algorithmic Logic

Your application's "intelligence" lies in its algorithms.

- **plan Algorithm:** This algorithm needs to determine which quests are fully completable. Your implementation should iterate through your collection of quests and, for each one, verify if the inventory's current stock meets all of its item requirements.
- **gap Algorithm:** This algorithm should calculate the items missing for a specific quest. It will need to compare the quest's requirements against the inventory and identify any shortfalls (item missing or quantity insufficient).
- **quest complete Algorithm:** This is a two-step process. First, it must verify that a quest is completable (you can reuse your plan logic for a single quest here). If it is, the second step is to consume the items by updating the inventory accordingly. If not, it should inform the user what is missing.

---

## Example Testbed & Usage Scenarios

### Testbed Files

#### config.json

```json
{
  "quest_file": "data/quests.json",
  "inventory_file": "data/inventory.json",
  "report_file": "reports/report.txt"
}
```

#### data/quests.json

```json
[
  {
    "name": "Goblin Camp",
    "items": {
      "sword": 1,
      "shield": 1,
      "potion": 2
    }
  },
  {
    "name": "Dragon Slayer",
    "items": {
      "sword": 1,
      "potion": 5,
      "fire_resist": 1,
      "rope": 1
    }
  },
  {
    "name": "Village Rescue",
    "items": {
      "sword": 1,
      "potion": 1,
      "torch": 2
    }
  },
  {
    "name": "Treasure Hunt",
    "items": {
      "map": 1,
      "shovel": 1,
      "rope": 2,
      "torch": 1
    }
  },
  {
    "name": "Bandit Hideout",
    "items": {
      "sword": 1,
      "shield": 1,
      "potion": 3,
      "rope": 1
    }
  },
  {
    "name": "Dark Cave",
    "items": {
      "torch": 3,
      "rope": 1,
      "potion": 2
    }
  },
  {
    "name": "Merchant Escort",
    "items": {
      "sword": 1,
      "shield": 1,
      "potion": 1
    }
  },
  {
    "name": "Lost Artifact",
    "items": {
      "map": 1,
      "shovel": 1,
      "torch": 2,
      "potion": 1
    }
  },
  {
    "name": "Quick Delivery",
    "items": {
      "rope": 1,
      "torch": 1
    }
  }
]
```

#### data/inventory.json (Initial State)

```json
{
  "sword": 2,
  "shield": 1,
  "potion": 3,
  "torch": 2,
  "rope": 1,
  "map": 0,
  "shovel": 0
}
```

#### batch_commands.txt (for the process command)

```
ADD potion 5
ADD fire_resist 2
ADD rope 2
ADD map 1
USE sword 3
ADD shovel 1
ADD torch 2
DROP potion 3
```

### Usage Scenario Walkthrough

1. **Start the Application in interactive mode:** The app loads `config.json`, then loads the initial quests and inventory data.

2. **List Quests:**
   ```
   > quest list
   1. Goblin Camp
   2. Dragon Slayer
   3. Village Rescue
   4. Treasure Hunt
   5. Bandit Hideout
   6. Dark Cave
   7. Merchant Escort
   8. Lost Artifact
   9. Quick Delivery
   ```

3. **Check Initial Plan:**
   ```
   > plan
   Completable Quests:
   - Goblin Camp
   - Quick Delivery
   ```

4. **View a Quest:**
   ```
   > quest view "Goblin Camp"
   Quest: Goblin Camp
   Required Items:
   - sword: 1
   - shield: 1
   - potion: 2
   ```

5. **Generate Missing Items List (Gap Analysis):**
   ```
   > quest gap "Dragon Slayer"
   Missing items for 'Dragon Slayer':
   - fire_resist: 1
   - potion: 2
   ```
   (The quest requires sword: 1, potion: 5, fire_resist: 1, rope: 1. With the initial inventory, the player has no fire_resist and only 3 potions, so 2 more potions are needed. Exact wording is up to you; the requirement is to show each missing item and the shortfall quantity.)

6. **Process a Batch File:**
   ```
   > inventory process batch_commands.txt
   Batch processing complete. See 'reports/report.txt' for details.
   ```
   - The `inventory.json` file is automatically updated.
   - The generated `reports/report.txt` should contain:
     ```
     SUCCESS: ADD potion 5
     SUCCESS: ADD fire_resist 2
     SUCCESS: ADD rope 2
     SUCCESS: ADD map 1
     ERROR: Cannot USE 3 sword, only 2 available.
     SUCCESS: ADD shovel 1
     SUCCESS: ADD torch 2
     ERROR: Unknown command 'DROP'.
     ```

7. **Check the Plan Again:** After the batch run, inventory has been updated (e.g. more potion, fire_resist, rope, map, shovel, torch; USE sword 3 failed so sword remains 2). The list of completable quests will have grown, for example:
   ```
   > plan
   Completable Quests:
   - Goblin Camp
   - Dragon Slayer
   - Village Rescue
   - Dark Cave
   - Merchant Escort
   - Quick Delivery
   ```

8. **Update Inventory Interactively:**
   ```
   > inventory use "potion" 2
   Successfully used 2 of 'potion'.
   ```
   (The `inventory.json` file is automatically saved with "potion" reduced by 2.)

9. **Complete a Quest:**
   ```
   > quest complete "Goblin Camp"
   Successfully completed 'Goblin Camp'. Inventory has been updated.
   ```
   (The `inventory.json` file is automatically saved with the items for Goblin Camp consumed: sword -1, shield -1, potion -2.)

10. **Exit:**
    ```
    > exit
    Inventory saved. Goodbye!
    ```

---

## Scoring System (100 Points Total)

| Category | Task Description | Points |
|----------|------------------|--------|
| **Architectural Design & Code Quality (20 points)** | Defines Quest and Inventory classes with clear responsibilities (data encapsulation, state management). | 5 |
| | Defines QuestLogManager as a controller, properly orchestrating interactions between models (Inventory/Quest) and user commands. | 5 |
| | Adheres to code quality standards (PEP 8 compliance, meaningful names, readability). | 5 |
| | Includes effective documentation (docstrings for classes/methods, comments for complex logic). | 5 |
| **Core Logic & Algorithms (25 points)** | Implements the plan algorithm correctly, handling cases with zero completable quests. | 10 |
| | Implements the quest gap algorithm correctly, handling cases with no missing items. | 5 |
| | Implements the quest complete logic, including the pre-check for completability and correct item consumption. | 10 |
| **Functionality & State Management (30 points)** | Implements dual-mode execution (manage vs. single command) and main application loop. | 5 |
| | Implements a robust command parser that correctly routes commands and arguments. | 5 |
| | Implements quest list/view commands with correct output formatting. | 5 |
| | Implements inventory add/use commands with correct state modification. | 5 |
| | Implements inventory process command, including file reading and sequential execution of sub-commands. | 10 |
| **Error Handling & Robustness (25 points)** | Gracefully handles file system errors (FileNotFoundError, etc) for all I/O operations. | 5 |
| | Implements robust input validation (correct number of arguments, correct data types for quantities). | 10 |
| | Implements state-based logical error handling (e.g., insufficient stock for inventory use or quest complete, quest not found). | 5 |
| | Handles invalid/unknown commands gracefully in both interactive and batch modes. | 5 |
