"""Unit tests for SpecsChecker."""

import pytest
from checkpcspecs.core.specs_checker import SpecsChecker
from checkpcspecs.core.models import SystemComponentStatus


class TestSpecsChecker:
    """Test SpecsChecker evaluation logic."""

    @pytest.fixture
    def checker(self):
        """Create SpecsChecker instance."""
        return SpecsChecker()

    def test_evaluate_os_windows_11(self, checker):
        """Test OS evaluation for Windows 11."""
        result = checker.evaluate_os("10", "10.0.22621")
        assert result == SystemComponentStatus.GOOD

    def test_evaluate_os_windows_10(self, checker):
        """Test OS evaluation for Windows 10."""
        result = checker.evaluate_os("10", "10.0.19044")
        assert result == SystemComponentStatus.GOOD

    def test_evaluate_os_windows_7(self, checker):
        """Test OS evaluation for Windows 7."""
        result = checker.evaluate_os("7", "6.1.7601")
        assert result == SystemComponentStatus.POOR

    def test_evaluate_architecture_x64(self, checker):
        """Test x64 architecture evaluation."""
        result = checker.evaluate_architecture("x64")
        assert result == SystemComponentStatus.GOOD

    def test_evaluate_architecture_x32(self, checker):
        """Test x32 architecture evaluation."""
        result = checker.evaluate_architecture("x32")
        assert result == SystemComponentStatus.POOR

    def test_evaluate_ram_excellent(self, checker):
        """Test RAM evaluation for excellent amount."""
        result = checker.evaluate_ram(16.0)
        assert result == SystemComponentStatus.EXCELLENT

    def test_evaluate_ram_good(self, checker):
        """Test RAM evaluation for good amount."""
        result = checker.evaluate_ram(6.0)
        assert result == SystemComponentStatus.GOOD

    def test_evaluate_ram_poor(self, checker):
        """Test RAM evaluation for poor amount."""
        result = checker.evaluate_ram(4.0)
        assert result == SystemComponentStatus.POOR

    def test_evaluate_cpu_excellent(self, checker):
        """Test CPU evaluation for excellent specs."""
        result = checker.evaluate_cpu("Intel Core i7-9700K", 8, 8)
        assert result == SystemComponentStatus.EXCELLENT

    def test_evaluate_cpu_with_bad_marker(self, checker):
        """Test CPU evaluation with bad marker."""
        result = checker.evaluate_cpu("Intel Atom Z3735F", 4, 4)
        assert result == SystemComponentStatus.POOR

    def test_evaluate_cpu_good(self, checker):
        """Test CPU evaluation for good specs."""
        result = checker.evaluate_cpu("Intel Core i3", 2, 4)
        assert result == SystemComponentStatus.GOOD

    def test_evaluate_disk_ssd_excellent(self, checker):
        """Test disk evaluation for SSD with good RAM."""
        result = checker.evaluate_disk("SSD", 8.0)
        assert result == SystemComponentStatus.EXCELLENT

    def test_evaluate_disk_ssd_with_low_ram(self, checker):
        """Test disk evaluation for SSD with low RAM."""
        result = checker.evaluate_disk("SSD", 4.5)
        assert result == SystemComponentStatus.GOOD

    def test_evaluate_disk_hdd_with_good_ram(self, checker):
        """Test disk evaluation for HDD with good RAM."""
        result = checker.evaluate_disk("HDD", 8.0)
        assert result == SystemComponentStatus.GOOD

    def test_evaluate_disk_hdd_poor(self, checker):
        """Test disk evaluation for HDD with low RAM."""
        result = checker.evaluate_disk("HDD", 4.0)
        assert result == SystemComponentStatus.POOR

    def test_evaluate_network_excellent(self, checker):
        """Test network evaluation for excellent performance."""
        result = checker.evaluate_network(100.0, 50.0, 20.0)
        assert result == SystemComponentStatus.EXCELLENT

    def test_evaluate_network_good_with_acceptable_ping(self, checker):
        """Test network evaluation with acceptable ping."""
        result = checker.evaluate_network(50.0, 20.0, 80.0)
        assert result == SystemComponentStatus.GOOD

    def test_evaluate_network_poor(self, checker):
        """Test network evaluation for poor performance."""
        result = checker.evaluate_network(10.0, 5.0)
        assert result == SystemComponentStatus.POOR

    def test_calculate_overall_score_excellent(self, checker):
        """Test overall score calculation for excellent PC."""
        score = checker.calculate_overall_score(
            SystemComponentStatus.EXCELLENT,
            SystemComponentStatus.GOOD,
            SystemComponentStatus.EXCELLENT,
            SystemComponentStatus.EXCELLENT,
            SystemComponentStatus.EXCELLENT
        )
        assert score >= 18

    def test_calculate_overall_score_poor(self, checker):
        """Test overall score calculation for poor PC."""
        score = checker.calculate_overall_score(
            SystemComponentStatus.POOR,
            SystemComponentStatus.POOR,
            SystemComponentStatus.POOR,
            SystemComponentStatus.POOR,
            SystemComponentStatus.POOR
        )
        assert score == -999

    def test_determine_requirement_level_exceeds(self, checker):
        """Test requirement level determination for exceeds."""
        from checkpcspecs.core.models import RequirementLevel
        result = checker.determine_requirement_level(20)
        assert result == RequirementLevel.EXCEEDS

    def test_determine_requirement_level_meets(self, checker):
        """Test requirement level determination for meets."""
        from checkpcspecs.core.models import RequirementLevel
        result = checker.determine_requirement_level(12)
        assert result == RequirementLevel.MEETS

    def test_determine_requirement_level_below(self, checker):
        """Test requirement level determination for below."""
        from checkpcspecs.core.models import RequirementLevel
        result = checker.determine_requirement_level(-10)
        assert result == RequirementLevel.BELOW
