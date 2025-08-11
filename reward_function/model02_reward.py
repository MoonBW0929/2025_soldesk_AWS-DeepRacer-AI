# model02 Reward Function

import math

def reward_function(params):
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    speed = params['speed']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']

    # 다음 두 waypoint를 가져오기
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # 트랙 방향 계산 (atan2로 각도 구하기)
    track_direction = math.degrees(math.atan2(
        next_point[1] - prev_point[1],
        next_point[0] - prev_point[0]
    ))

    # 트랙 방향과 차량 방향 차이
    direction_diff = abs(track_direction - heading)
    direction_diff = min(direction_diff, 360 - direction_diff)  # 각도 wraparound 보정

    # 직선과 커브 판단 기준
    STRAIGHT_THRESHOLD = 5.0  # degrees

    # 기본 보상
    reward = 1.0

    if direction_diff < STRAIGHT_THRESHOLD:
        # 직선 구간
        # 속도가 높을수록 큰 보상
        reward += speed ** 2
    else:
        # 커브 구간
        # 인코스로 달릴수록 보상
        marker = 0.25 * track_width  # 트랙 중앙 기준 거리
        if distance_from_center <= marker:
            reward += 2.0  # 인코스 보상
        else:
            reward += 0.5  # 아웃코스 또는 중간 위치

        # 커브 구간 속도 감속
        if speed > 2.0:
            reward *= 0.5

    return float(reward)