import grpc
import course_service_pb2
import course_service_pb2_grpc


def run():
    # Установка соединения с сервером
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = course_service_pb2_grpc.CourseServiceStub(channel)

        # Формирование запроса
        request = course_service_pb2.GetCourseRequest(course_id="api-course")

        # Вызов метода и получение ответа
        response = stub.GetCourse(request)

        # Вывод ответа
        print(f"course_id: \"{response.course_id}\"")
        print(f"title: \"{response.title}\"")
        print(f"description: \"{response.description}\"")


if __name__ == '__main__':
    run()