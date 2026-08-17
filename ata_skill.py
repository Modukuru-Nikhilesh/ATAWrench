import json

class AviationATASkill:
    def __init__(self, database_file):
        with open(database_file, "r", encoding="utf-8") as file:
            self.database = self._sanitize_data(json.load(file))

    def _sanitize_data(self, data):
        if isinstance(data, dict):
            return {k.strip(): self._sanitize_data(v) for k, v in data.items()}
        if isinstance(data, list):
            return [self._sanitize_data(i) for i in data]
        if isinstance(data, str):
            return data.strip()
        return data

    def search_recursive(self, data, code):
        for ata_code, details in data.items():
            if ata_code == code:
                return {
                    "ata_code": ata_code,
                    "name": details.get("name", "N/A"),
                    "aircraft": details.get("aircraft", []),
                    "description": details.get("description", "N/A"),
                    "components": details.get("components", []),
                    "manuals": details.get("manuals", []),
                    "symptoms": details.get("symptoms", []),
                    "possible_causes": details.get("possible_causes", []),
                    "bite_tests": details.get("bite_tests", []),
                    "corrective_actions": details.get("corrective_actions", []),
                    "preventive_actions": details.get("preventive_actions", [])
                }
            if isinstance(details, dict) and "subchapters" in details:
                result = self.search_recursive(details["subchapters"], code)
                if result:
                    return result
        return None

    def search_ata(self, code):
        result = self.search_recursive(self.database, code.strip())
        if result:
            return result
        return {"error": f"ATA Code {code} Not Found"}

    def list_codes(self):
        codes = []
        for chapter, details in self.database.items():
            if isinstance(details, dict) and "subchapters" in details:
                for sub, d in details["subchapters"].items():
                    codes.append({"code": sub, "name": d.get("name", "")})
        return codes