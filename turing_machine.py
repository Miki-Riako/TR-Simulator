import sys

MAXSIZE = 100

class TuringMachine:
    def __init__(self):
        self.exitRuler = False
        self.turingRuler = ""
        self.paper = ""
        self.turingRulerList = []
        self.rulers = []
        self.state = ''
        self.rulersLen = 0
        self.paperPtr = 0

    def readRuler(self, turingRuler):
        # try:
        #     with open("./ruler.txt", "r") as file:
        #         turingRuler += file.read()
        # except FileNotFoundError:
        #     print("Error: Rulers Loading Error!")
        #     sys.exit(1)
        ...

    def printPaper(self):
        input_str = f"State: q{self.state}, "
        input_str += self.paper[:self.paperPtr] + "->" + self.paper[self.paperPtr:]
        print(input_str)

    def checkPaper(self):
        if self.state == '#':
            print("The paper is Readable.")
        if self.paperPtr == len(self.paper):
            self.paper += 'B'

    def loadRuler(self):
        # if not self.exitRuler:
        #     self.readRuler(self.turingRuler)
        #     lines = self.turingRuler.split('\n')
        #     for i, line in enumerate(lines):
        #         if line:
        #             self.turingRulerList.append(line)
        #             if self.rulersLen >= MAXSIZE:
        #                 print("Error: Rulers Length Error!")
        #                 return
        #             self.rulers[i] = [line[0], line[2], line[4], line[6], line[8]]
        #             self.rulersLen += 1
        #     self.exitRuler = True
        # else:
        #     print("Error: Rulers Already Loaded!")
        #     return
        self.rulers += [['1', '0', '2', 'B', 'R']]
        self.rulers += [['2', '0', '3', 'X', 'R']]
        self.rulers += [['2', 'X', '2', 'X', 'R']]
        self.rulers += [['2', 'B', '#', 'B', 'R']]
        self.rulers += [['3', '0', '4', '0', 'R']]
        self.rulers += [['3', 'X', '3', 'X', 'R']]
        self.rulers += [['3', 'B', '5', 'B', 'L']]
        self.rulers += [['4', '0', '3', 'X', 'R']]
        self.rulers += [['4', 'X', '4', 'X', 'R']]
        self.rulers += [['5', '0', '5', '0', 'L']]
        self.rulers += [['5', 'X', '5', 'X', 'L']]
        self.rulers += [['5', 'B', '2', 'B', 'R']]
        self.rulersLen = 12
        self.exitRuler = True

    def inputPaper(self):
        self.state = '1'
        self.paperPtr = 1
        print("Paper Loading Success!")
        input_str = input("Enter the paper content: ")
        self.paper = 'B' + input_str
        self.printPaper()

    def move(self):
        if not self.exitRuler:
            return
        if self.state == '#':
            print("The paper is Readable.")
            return
        for i in range(self.rulersLen):
            if self.rulers[i][0] == self.state and self.rulers[i][1] == self.paper[self.paperPtr]:
                self.state = self.rulers[i][2]
                self.paper = self.paper[:self.paperPtr] + self.rulers[i][3] + self.paper[self.paperPtr + 1:]
                if self.rulers[i][4] == 'L':
                    self.paperPtr -= 1
                elif self.rulers[i][4] == 'R':
                    self.paperPtr += 1
                break
        else:
            print("The paper is unreadable.")
            return
        self.printPaper()
        self.checkPaper()


if __name__ == "__main__":
    tm = TuringMachine()
    tm.loadRuler()
    tm.inputPaper()
    while True:
        command = input("Enter command (move/exit): ").strip().lower()
        if command == "move":
            tm.move()
        elif command == "exit":
            break
