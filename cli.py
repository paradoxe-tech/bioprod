from main import Main

if __name__ == "__main__":
    process = Main("config/config.json")
    
    while True:
        try:
            cmd = input("run > ")
            output = process.execute(cmd)
            print(output)
        except KeyboardInterrupt:
            break
        except Exception as e:
            process.logger.error(e)