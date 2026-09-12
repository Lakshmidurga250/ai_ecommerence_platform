"""
Advanced Logistics & Delivery Route Optimization Engine.
Calculates optimal fulfillment paths, multi-node delivery routing (Dijkstra / TSP heuristic),
vehicle capacity constraints, delivery cost, and carbon footprint emissions.
"""
from typing import Dict, Any, List, Tuple, Optional
import heapq
import math


class LogisticsRouteOptimizer:
    """
    Logistics network router evaluating graph distances, transit times, and vehicle allocation.
    """

    # Major fulfillment transit nodes (Coordinates: lat, lon)
    HUBS = {
        "DEL": {"name": "Delhi NCR Mega Hub", "coords": (28.6139, 77.2090), "type": "PRIMARY"},
        "BOM": {"name": "Mumbai Western Hub", "coords": (19.0760, 72.8777), "type": "PRIMARY"},
        "BLR": {"name": "Bengaluru Southern Hub", "coords": (12.9716, 77.5946), "type": "PRIMARY"},
        "CCU": {"name": "Kolkata Eastern Hub", "coords": (22.5726, 88.3639), "type": "REGIONAL"},
        "HYD": {"name": "Hyderabad Central Hub", "coords": (17.3850, 78.4867), "type": "REGIONAL"},
        "MAA": {"name": "Chennai Coastal Hub", "coords": (13.0827, 80.2707), "type": "REGIONAL"},
        "AMD": {"name": "Ahmedabad Transit Hub", "coords": (23.0225, 72.5714), "type": "REGIONAL"},
        "PNQ": {"name": "Pune Express Hub", "coords": (18.5204, 73.8567), "type": "FEEDER"},
        "JAI": {"name": "Jaipur Feeder Hub", "coords": (26.9124, 75.7873), "type": "FEEDER"},
        "LKO": {"name": "Lucknow Central Hub", "coords": (26.8467, 80.9462), "type": "FEEDER"},
    }

    # Weighted network graph: (from_node, to_node, distance_km, avg_transit_hours)
    TRANSIT_CORRIDORS = [
        ("DEL", "JAI", 280, 5.0),
        ("DEL", "LKO", 550, 9.0),
        ("DEL", "AMD", 930, 16.0),
        ("DEL", "BOM", 1420, 24.0),
        ("DEL", "CCU", 1530, 26.0),
        ("BOM", "PNQ", 150, 3.5),
        ("BOM", "AMD", 530, 9.0),
        ("BOM", "HYD", 710, 13.0),
        ("BOM", "BLR", 980, 17.0),
        ("BLR", "MAA", 350, 6.0),
        ("BLR", "HYD", 570, 10.0),
        ("BLR", "PNQ", 840, 15.0),
        ("HYD", "MAA", 630, 11.0),
        ("HYD", "CCU", 1490, 25.0),
        ("CCU", "LKO", 980, 17.0),
    ]

    def __init__(self):
        # Build adjacency graph
        self.graph = {hub: [] for hub in self.HUBS}
        for u, v, dist, hrs in self.TRANSIT_CORRIDORS:
            self.graph[u].append((v, dist, hrs))
            self.graph[v].append((u, dist, hrs))  # Bidirectional

    def find_optimal_transit_route(
        self,
        origin_hub: str,
        destination_hub: str
    ) -> Dict[str, Any]:
        """
        Uses Dijkstra's algorithm to determine the shortest and fastest fulfillment route.
        """
        origin = origin_hub.upper()
        dest = destination_hub.upper()

        if origin not in self.HUBS:
            origin = "DEL"
        if dest not in self.HUBS:
            dest = "BLR"

        if origin == dest:
            return {
                "origin": origin,
                "destination": dest,
                "total_distance_km": 25,
                "total_transit_hours": 2.0,
                "route_path": [origin],
                "path_names": [self.HUBS[origin]["name"]],
                "estimated_shipping_cost": 65.0,
                "carbon_kg_co2": 2.1,
                "route_type": "LOCAL_METRO_INTRA_CITY"
            }

        # Dijkstra's shortest path
        pq = [(0.0, 0.0, origin, [origin])]  # (distance, hours, current_node, path)
        visited = set()

        shortest_dist = float("inf")
        best_path = []
        best_hours = float("inf")

        while pq:
            d, h, curr, path = heapq.heappop(pq)

            if curr == dest:
                shortest_dist = d
                best_hours = h
                best_path = path
                break

            if curr in visited:
                continue
            visited.add(curr)

            for neighbor, edge_dist, edge_hrs in self.graph.get(curr, []):
                if neighbor not in visited:
                    heapq.heappush(pq, (d + edge_dist, h + edge_hrs, neighbor, path + [neighbor]))

        if not best_path:
            # Direct approximation fallback
            coord_origin = self.HUBS[origin]["coords"]
            coord_dest = self.HUBS[dest]["coords"]
            approx_dist = round(self._haversine(coord_origin, coord_dest) * 1.25, 1)
            approx_hours = round(approx_dist / 60.0, 1)
            best_path = [origin, dest]
            shortest_dist = approx_dist
            best_hours = approx_hours

        # Commercial and Environmental metrics
        shipping_cost = round(80.0 + (shortest_dist * 0.12), 2)
        carbon_emissions = round((shortest_dist * 0.115), 2)  # kg CO2 for standard express carrier

        return {
            "origin": origin,
            "origin_name": self.HUBS[origin]["name"],
            "destination": dest,
            "destination_name": self.HUBS[dest]["name"],
            "total_distance_km": shortest_dist,
            "total_transit_hours": best_hours,
            "estimated_delivery_days": max(1, math.ceil(best_hours / 24.0)),
            "route_path": best_path,
            "path_names": [self.HUBS[code]["name"] for code in best_path],
            "estimated_shipping_cost": shipping_cost,
            "carbon_kg_co2": carbon_emissions,
            "eco_tier": "CARBON_NEUTRAL_ELIGIBLE" if carbon_emissions < 100 else "STANDARD_FREIGHT",
            "algorithm_used": "DIJKSTRA_SHORTEST_PATH"
        }

    def optimize_delivery_sequence_tsp(
        self,
        stop_codes: List[str]
    ) -> Dict[str, Any]:
        """
        Solves multi-stop delivery sequence using nearest-neighbor TSP approximation.
        """
        valid_stops = [s.upper() for s in stop_codes if s.upper() in self.HUBS]
        if len(valid_stops) <= 1:
            return {"sequence": valid_stops, "total_km": 0.0}

        unvisited = set(valid_stops[1:])
        current = valid_stops[0]
        sequence = [current]
        total_dist = 0.0

        while unvisited:
            nearest = min(
                unvisited,
                key=lambda n: self._haversine(self.HUBS[current]["coords"], self.HUBS[n]["coords"])
            )
            dist = self._haversine(self.HUBS[current]["coords"], self.HUBS[nearest]["coords"])
            total_dist += dist
            current = nearest
            sequence.append(current)
            unvisited.remove(nearest)

        return {
            "optimized_delivery_sequence": sequence,
            "sequence_names": [self.HUBS[c]["name"] for c in sequence],
            "total_estimated_km": round(total_dist, 1),
            "estimated_fuel_liters": round(total_dist * 0.08, 1),
            "algorithm": "TSP_NEAREST_NEIGHBOR_APPROXIMATION"
        }

    def _haversine(self, c1: Tuple[float, float], c2: Tuple[float, float]) -> float:
        lat1, lon1 = math.radians(c1[0]), math.radians(c1[1])
        lat2, lon2 = math.radians(c2[0]), math.radians(c2[1])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return 6371.0 * c  # Earth radius in km
