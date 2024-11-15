from DataDispatcher import DataDispatcher

grid_dispatcher = DataDispatcher(
    "PLC",
    "grid_logs",
    "smart_grid_stability_augmented.csv",
    5555,
    35000,
    1
)
grid_dispatcher.start()
