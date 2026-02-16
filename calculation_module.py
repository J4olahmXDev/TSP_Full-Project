import math

def get_dist(c1, c2):
    """คำนวณระยะห่างระหว่างเมือง 2 เมือง"""
    return math.sqrt((c1['x'] - c2['x'])**2 + (c1['y'] - c2['y'])**2)

def solve_tsp_nearest_neighbor(cities):
    """
    Algorithm: Nearest Neighbor Method
    คืนค่า: (Total Distance, Route Path List)
    """
    if not cities:
        return 0, []
    
    # Clone list เพื่อไม่ให้กระทบข้อมูลหลัก
    unvisited = cities[:]
    
    # เริ่มต้นที่เมืองแรกที่ User เพิ่มเข้ามา
    current_city = unvisited.pop(0)
    route_path = [current_city]
    total_distance = 0

    while unvisited:
        # หาเมืองที่ใกล้ current_city ที่สุด (Greedy Approach)
        nearest_city = min(unvisited, key=lambda city: get_dist(current_city, city))
        
        # บวกระยะทาง
        total_distance += get_dist(current_city, nearest_city)
        
        # Move ไปเมืองนั้น
        current_city = nearest_city
        route_path.append(current_city)
        unvisited.remove(current_city)

    # วนกลับจุดเริ่มต้น (Loop back to start)
    if len(route_path) > 1:
        total_distance += get_dist(route_path[-1], route_path[0])
        route_path.append(route_path[0])
        
    return total_distance, route_path