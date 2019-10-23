# # import keyboard
# # keyboard.add_hotkey('ctrl+shift+t',print,args=("manas","satti"),timeout=1,trigger_on_release=False)
# import time
# start_time = time.time()
# time.sleep(10)
# print(time.time()-start_time)
# import csv
# def csv_writer(filename, data):
#     with open(filename, "a") as csv_file:
#         writer = csv.writer(csv_file, delimiter=',')
#         for line in data:
#             writer.writerow(line)

# key_press_rec = [[0,'Start time of asana'],[5,"Start time of asana's hold-time"],[15,"End time of asana's hold-time"],[20,"End time of asana"]]

# csv_writer("testing.csv",key_press_rec)
# apple = [[0,1],[2,3],[4,5]]
# print([[-1,-2]]+apple)