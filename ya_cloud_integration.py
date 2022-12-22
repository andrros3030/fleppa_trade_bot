import yandexcloud
from constants import SERVICE_ACC_PRIVATE_KEY

# from yandex.cloud.resourcemanager.v1.cloud_service_pb2 import ListCloudsRequest
# from yandex.cloud.resourcemanager.v1.cloud_service_pb2_grpc import CloudServiceStub
# from yandex.cloud.
from yandex.cloud.compute.v1.image_service_pb2 import GetImageLatestByFamilyRequest


def main():
    interceptor = yandexcloud.RetryInterceptor(max_retry_count=5, retriable_codes=[grpc.StatusCode.UNAVAILABLE])
    sdk = yandexcloud.SDK(iam_token=SERVICE_ACC_PRIVATE_KEY)


if __name__ == '__main__':
    main()
# def handler(event, context):
#     cloud_service = yandexcloud.SDK().client(CloudServiceStub)
#     clouds = {}
#     for c in cloud_service.List(ListCloudsRequest()).clouds:
#         clouds[c.id] = c.name
#     return clouds
