#ifndef TASK_HPP
#define TASK_HPP

enum TaskState {
  RUNNING = 1,
  IDLE = 0
};

class Task {
  unsigned long period;
  unsigned long previousMillis;
  TaskState state;

protected:
  virtual void update() = 0;

public:
  Task(unsigned long period) : previousMillis(0), period(period), state(TaskState::IDLE) {}

  void run() {
    this->update();
  }

  TaskState getState() {
    unsigned long currentMillis = millis();

    // counter overflow detection:
    if (currentMillis < previousMillis) {
      previousMillis = currentMillis;
      Serial.println("Task detected counter overflow.");
      this->state = TaskState::IDLE;
    }
    // if the period have passed, run job:
    else if (currentMillis - previousMillis >= this->period) {
      previousMillis = currentMillis;
      this->state = TaskState::RUNNING;
    } else {
      this->state = TaskState::IDLE;
    }

    return this->state;
  }
};

#endif