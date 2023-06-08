from evoflow.services.ocr.ocr_service import OCRService


class ServicesController:
    def __init__(self):
        self.running_services = {}
        self.SERVICES_LIST = {"ocr": OCRService}

    def start_services(self, service_id, **args):
        try:
            service = self.SERVICES_LIST[service_id](**args)
            self.running_services[service_id] = service
        except Exception as e:
            return e
        return True

    def get_services_name(self):
        services_names = list(self.SERVICES_LIST.keys())
        return services_names

    def run_service(self, service_id, data, **args):
        if service_id not in self.running_services:
            return "Service not started"
        sevice = self.running_services[service_id]
        result = sevice.run(data, **args)
        return result


if __name__ == "__main__":
    import cv2

    service = ServicesController().start_services(
        "ocr", engine_name="easyocr", languages=["en", "ja"]
    )
    service: OCRService
    mat = cv2.imread("data/document_jp.PNG")
    res = service.ocr(mat)
    print(res)
