class TestQ4:
    def test_export_creates_json_file(self, tmp_path):
        import be
        export_dir = str(tmp_path / "q4_test")
        be.export_db_to_json(export_dir)
        import os
        assert os.path.exists(os.path.join(export_dir, "data.json"))

    def test_export_contains_all_tables(self, tmp_path):
        import be, json, os
        export_dir = str(tmp_path / "q4_test")
        be.export_db_to_json(export_dir)
        with open(os.path.join(export_dir, "data.json")) as f:
            data = json.load(f)
        for table in ["facility", "supplier", "product", "warehouse", "consumption"]:
            assert table in data

    def test_export_facility_has_3_records(self, tmp_path):
        import be, json, os
        export_dir = str(tmp_path / "q4_test")
        be.export_db_to_json(export_dir)
        with open(os.path.join(export_dir, "data.json")) as f:
            data = json.load(f)
        assert len(data["facility"]) >= 3