from collections import defaultdict

class Metrics:
    def __init__(self):
        self.command_counters = defaultdict(int)
        self.reports_generated = 0
    
    def increment_command_counter(self, command: str):
        """Увеличение счетчика команд"""
        self.command_counters[command] += 1
    
    def increment_reports_generated(self):
        """Увеличение счетчика отчетов"""
        self.reports_generated += 1
    
    def get_stats(self) -> dict:
        """Получение статистики"""
        return {
            'commands': dict(self.command_counters),
            'reports_generated': self.reports_generated
        }

metrics = Metrics()
