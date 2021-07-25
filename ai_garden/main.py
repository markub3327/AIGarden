import os

from ai_garden import AIGarden


def clear():
    os.system("clear")


if __name__ == "__main__":
    # Init AI garden
    my_ai_garden = AIGarden()
    watering_time = 60

    # Main loop
    while True:
        print("AIGarden 🚰🥕🍅")
        print("Bc. Martin Kubovčík")
        print("https://github.com/markub3327/AIGarden")
        print()
        print("        1  Watering 🚰")
        print("        2  Scan 👀")
        print("        3  Settings ⚙️")
        print("        q  Quit 🚪")
        print()
        cmd = input(">> ")

        if cmd == "1":
            clear()  # clear console
            end = False
            while end is False:
                print("Select pump")
                print("        1  Pump 0")
                print("        2  Pump 1")
                print("        q  Quit 🚪")
                print()
                cmd = input(">> ")

                if cmd == "1":
                    my_ai_garden.watering(0, duration=watering_time)
                elif cmd == "2":
                    my_ai_garden.watering(1, duration=watering_time)
                elif cmd == "q":
                    clear()  # clear console
                    break
                else:
                    print("Bad command was eneterd.")
        elif cmd == "2":
            clear()  # clear console
            print("Scanning ...")
            my_ai_garden.readHumidity()
            my_ai_garden.readSoilMoisture()
            print()
        elif cmd == "3":
            clear()  # clear console
            end = False
            while end is False:
                print("Settings ⚙️")
                print("        1  Watering Time")
                print("        q  Quit 🚪")
                print()
                cmd = input(">> ")

                if cmd == "1":
                    cmd = input(f"Watering Time ({watering_time}) : ")
                    watering_time = int(cmd)
                    break
                if cmd == "q":
                    clear()  # clear console
                    break
                else:
                    print("Bad command was eneterd.")
        elif cmd == "q":
            my_ai_garden.close()
            print("Terminated by user 👋👋👋")
            exit()
        else:
            print("Bad command was eneterd.")
