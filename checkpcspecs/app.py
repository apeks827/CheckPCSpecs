"""Main application controller."""

import asyncio
import logging
import multiprocessing
from typing import Optional

import nest_asyncio

from .core import SpecsChecker
from .network import SpeedTester, PingTester, NetworkEvaluator
from .ui import MainWindow
from .ui.components import ResultColor
from .utils import ScoreCalculator

nest_asyncio.apply()
logger = logging.getLogger(__name__)


class Application:
    """Main application controller."""

    def __init__(self):
        self.window = MainWindow()
        self.specs_checker = SpecsChecker()
        self.username: Optional[str] = None
        self.component_scores: list[int] = []

    def _add_os_result(self):
        """Display OS check results."""
        os_result = self.specs_checker.check_os()
        self.component_scores.append(os_result.score)

        color_map = {
            2: ResultColor.GOOD,
            1: ResultColor.GOOD,
            0: ResultColor.WARNING,
            -1: ResultColor.ERROR
        }

        display_text = "11" if os_result.rating == 2 else os_result.version
        self.window.result_display.add_result(
            "Версия ОС:",
            display_text,
            color_map.get(os_result.rating, ResultColor.NEUTRAL)
        )

    def _add_arch_result(self):
        """Display architecture check results."""
        arch_result = self.specs_checker.check_architecture()
        self.component_scores.append(arch_result.score)

        color = ResultColor.GOOD if arch_result.rating == 1 else ResultColor.ERROR
        text = "x64" if arch_result.rating == 1 else "x32"

        self.window.result_display.add_result(
            "Разрядность ОС:",
            text,
            color
        )

    def _add_ram_result(self):
        """Display RAM check results."""
        ram_result = self.specs_checker.check_ram()
        self.component_scores.append(ram_result.score)

        color_map = {
            1: ResultColor.GOOD,
            0: ResultColor.WARNING,
            -1: ResultColor.ERROR
        }

        self.window.result_display.add_result(
            "RAM:",
            f"{ram_result.total_gb:.1f} GB",
            color_map.get(ram_result.rating, ResultColor.NEUTRAL)
        )

    def _add_cpu_result(self):
        """Display CPU check results."""
        cpu_result = self.specs_checker.check_cpu()
        self.component_scores.append(cpu_result.score)

        color_map = {
            1: ResultColor.GOOD,
            0: ResultColor.WARNING,
            -1: ResultColor.ERROR
        }

        self.window.result_display.add_result(
            "CPU:",
            cpu_result.name,
            color_map.get(cpu_result.rating, ResultColor.NEUTRAL)
        )

    async def _add_disk_result(self):
        """Display disk check results (async)."""
        disk_result = await self.specs_checker.check_disk_async()
        self.component_scores.append(disk_result.score)

        color_map = {
            1: ResultColor.GOOD,
            0: ResultColor.WARNING,
            -1: ResultColor.ERROR,
            -2: ResultColor.ERROR
        }

        text_map = {
            1: "SSD",
            0: "HDD or eMMC",
            -1: "HDD or eMMC",
            -2: "Определить невозможно"
        }

        self.window.result_display.add_result(
            "Тип диска:",
            text_map.get(disk_result.rating, "Unknown"),
            color_map.get(disk_result.rating, ResultColor.NEUTRAL)
        )

    async def _add_network_results(self):
        """Display network test results (async)."""
        # Show loading message
        loading_label = self.window.result_display.add_result(
            "Скорость сети:",
            "Подождите...",
            ResultColor.NEUTRAL
        )

        # Run tests
        ping_result = await asyncio.to_thread(PingTester.test)
        speed_result = await asyncio.to_thread(SpeedTester.test)

        current_row = self.window.result_display.get_current_row() - 1

        if speed_result.success and ping_result.success:
            # Evaluate network
            evaluation = NetworkEvaluator.evaluate(
                speed_result.download,
                speed_result.upload,
                ping_result.latency
            )
            self.component_scores.append(evaluation.score_points)

            # Update first row with download speed
            loading_label.config(
                text=f"Загрузка: {speed_result.download} Mbps",
                fg=ResultColor.GOOD if speed_result.download >= 20 else ResultColor.ERROR
            )

            # Add upload and ping
            self.window.result_display.add_result(
                "",
                f"Отдача: {speed_result.upload} Mbps",
                ResultColor.GOOD if speed_result.upload >= 10 else ResultColor.ERROR
            )

            ping_color = ResultColor.GOOD if ping_result.latency <= 30 else (
                ResultColor.WARNING if ping_result.latency <= 100 else ResultColor.ERROR
            )
            self.window.result_display.add_result(
                "",
                f"Пинг: {ping_result.latency} ms",
                ping_color
            )
        else:
            # Failed
            self.component_scores.append(0)
            loading_label.set_error("Скорость соединения определить невозможно")

            if ping_result.success:
                ping_color = ResultColor.GOOD if ping_result.latency <= 30 else (
                    ResultColor.WARNING if ping_result.latency <= 100 else ResultColor.ERROR
                )
                self.window.result_display.add_result(
                    "",
                    f"Пинг: {ping_result.latency} ms",
                    ping_color
                )

    def _add_final_verdict(self):
        """Display final PC verdict."""
        pc_score = ScoreCalculator.calculate(*self.component_scores)

        import tkinter as tk
        verdict_label = tk.Label(
            self.window.root,
            text=pc_score.verdict_text_ru,
            fg=pc_score.verdict_color,
            font=("Arial", 15 if pc_score.verdict_color == "green" else 12)
        )
        verdict_label.grid(
            column=2,
            row=self.window.result_display.get_current_row(),
            sticky="w"
        )

    async def _run_tests(self):
        """Run all PC tests."""
        try:
            # Synchronous tests
            self._add_os_result()
            self._add_arch_result()
            self._add_ram_result()
            self._add_cpu_result()

            # Asynchronous tests
            await self._add_disk_result()
            await self._add_network_results()

            # Final verdict
            self._add_final_verdict()

        except Exception as e:
            logger.exception(f"Error during tests: {e}")

    def _on_start(self, username: str):
        """Handle test start.
        
        Args:
            username: User's full name
        """
        self.username = username
        asyncio.run(self.window.run_async_task(self._run_tests()))

    def run(self):
        """Run the application."""
        # Setup UI
        self.window.setup_name_input(self._on_start)
        self.window.add_quit_button()

        # Start event loop
        self.window.run()


def main():
    """Entry point for the application."""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create and run app
    app = Application()
    app.run()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
