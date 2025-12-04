"""Integration tests for full system check."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from checkpcspecs.core.specs_checker import SpecsChecker
from checkpcspecs.core.models import SystemComponentStatus, RequirementLevel


class TestFullSystemCheck:
    """Integration tests for complete system evaluation."""

    @pytest.fixture
    def checker(self):
        """Create SpecsChecker instance."""
        return SpecsChecker()

    def test_high_end_system_evaluation(self, checker, mock_high_spec_system):
        """Test evaluation of high-end system."""
        # Evaluate all components
        os_status = checker.evaluate_os(
            mock_high_spec_system.os_version,
            mock_high_spec_system.os_release
        )
        arch_status = checker.evaluate_architecture(
            mock_high_spec_system.architecture
        )
        ram_status = checker.evaluate_ram(mock_high_spec_system.ram_gb)
        cpu_status = checker.evaluate_cpu(
            mock_high_spec_system.cpu_brand,
            mock_high_spec_system.cpu_cores,
            mock_high_spec_system.cpu_threads
        )
        disk_status = checker.evaluate_disk(
            mock_high_spec_system.disk_type,
            mock_high_spec_system.ram_gb
        )

        # All should be good or excellent
        assert os_status in [SystemComponentStatus.GOOD, SystemComponentStatus.EXCELLENT]
        assert arch_status == SystemComponentStatus.GOOD
        assert ram_status == SystemComponentStatus.EXCELLENT
        assert cpu_status == SystemComponentStatus.EXCELLENT
        assert disk_status == SystemComponentStatus.EXCELLENT

        # Overall score should be high
        score = checker.calculate_overall_score(
            os_status, arch_status, ram_status, cpu_status, disk_status
        )
        assert score >= 18

        # Should exceed requirements
        level = checker.determine_requirement_level(score)
        assert level == RequirementLevel.EXCEEDS

    def test_low_end_system_evaluation(self, checker, mock_low_spec_system):
        """Test evaluation of low-end system."""
        # Evaluate all components
        os_status = checker.evaluate_os(
            mock_low_spec_system.os_version,
            mock_low_spec_system.os_release
        )
        arch_status = checker.evaluate_architecture(
            mock_low_spec_system.architecture
        )
        ram_status = checker.evaluate_ram(mock_low_spec_system.ram_gb)
        cpu_status = checker.evaluate_cpu(
            mock_low_spec_system.cpu_brand,
            mock_low_spec_system.cpu_cores,
            mock_low_spec_system.cpu_threads
        )
        disk_status = checker.evaluate_disk(
            mock_low_spec_system.disk_type,
            mock_low_spec_system.ram_gb
        )

        # Most should be poor
        assert os_status == SystemComponentStatus.POOR
        assert arch_status == SystemComponentStatus.POOR
        assert ram_status == SystemComponentStatus.POOR
        assert cpu_status == SystemComponentStatus.POOR

        # Overall score should be low
        score = checker.calculate_overall_score(
            os_status, arch_status, ram_status, cpu_status, disk_status
        )
        assert score < 0

        # Should be below requirements
        level = checker.determine_requirement_level(score)
        assert level == RequirementLevel.BELOW

    def test_mid_range_system_evaluation(self, checker):
        """Test evaluation of mid-range system."""
        # Evaluate mid-range components
        os_status = checker.evaluate_os("10", "10.0.19044")
        arch_status = checker.evaluate_architecture("x64")
        ram_status = checker.evaluate_ram(8.0)
        cpu_status = checker.evaluate_cpu("Intel Core i5-8400", 6, 6)
        disk_status = checker.evaluate_disk("SSD", 8.0)

        # Should be mostly good
        assert os_status == SystemComponentStatus.GOOD
        assert arch_status == SystemComponentStatus.GOOD
        assert ram_status in [SystemComponentStatus.GOOD, SystemComponentStatus.EXCELLENT]
        assert cpu_status == SystemComponentStatus.EXCELLENT
        assert disk_status == SystemComponentStatus.EXCELLENT

        # Score should be in meets range
        score = checker.calculate_overall_score(
            os_status, arch_status, ram_status, cpu_status, disk_status
        )
        assert 10 <= score < 18

        # Should meet requirements
        level = checker.determine_requirement_level(score)
        assert level == RequirementLevel.MEETS
