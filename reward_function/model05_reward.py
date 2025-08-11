# model05 Reward Function

import math

def reward_function(params):
    
    speed = params['speed']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    all_wheels_on_track = params['all_wheels_on_track']

    ##############################

    def is_corner(params, angle_threshold=10):

        waypoints = params['waypoints']
        prev_i, next_i = params['closest_waypoints']
    
        # 주변 3개 점을 가져오기 위해 이전과 이후 waypoint 계산
        if prev_i - 1 < 0 or next_i + 1 >= len(waypoints):
            return False  # 판단 불가 -> 직선 처리
    
        point_a = waypoints[prev_i - 1]
        point_b = waypoints[prev_i]
        point_c = waypoints[next_i]
    
        def angle_between(p1, p2):
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            return math.degrees(math.atan2(dy, dx))
    
        angle1 = angle_between(point_a, point_b)
        angle2 = angle_between(point_b, point_c)
    
        angle_diff = abs(angle1 - angle2)
        if angle_diff > 180:
            angle_diff = 360 - angle_diff
    
        return angle_diff > angle_threshold

    ##############################

    # 기본 보상
    reward = 1.0

    if is_corner(params):
        # 커브 구간
        # 인코스로 달릴수록 보상
        marker = 0.25 * track_width  # 트랙 중앙 기준 거리
        if distance_from_center <= marker:
            reward += 2.0  # 인코스 보상
        else:
            reward += 0.5  # 아웃코스 또는 중간 위치

        # 커브 구간 속도 감속
        if speed > 1.5:
            reward *= 0.2
    else:
        # 직선 구간
        # 속도가 높을수록 큰 보상
        reward += speed ** 2

    # 최대한 코스 안쪽을 유지하도록 보상
    if not all_wheels_on_track:
        reward += 0.1
    else:
        reward += 1
    
    return float(reward)