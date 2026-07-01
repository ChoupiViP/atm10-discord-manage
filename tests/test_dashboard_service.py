from bot.services.dashboard_service import DashboardService


def test_dashboard_service_lifecycle(tmp_path):
    storage_path = tmp_path / "dashboard.json"
    dashboard = DashboardService(storage_path)

    assert not dashboard.exists()

    dashboard.save(guild_id=123, channel_id=456, message_id=789)

    assert dashboard.exists()
    assert dashboard.get_guild_id() == 123
    assert dashboard.get_channel_id() == 456
    assert dashboard.get_message_id() == 789
    assert dashboard.get_data()["created_at"] is not None

    dashboard.clear()

    assert not dashboard.exists()
    assert dashboard.get_data()["message_id"] is None
