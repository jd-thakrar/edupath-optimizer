"""
Knowledge Dependency Graph
Represents prerequisite relationships between subjects
Enables forward risk propagation
"""

import networkx as nx
from typing import Dict, List, Any, Set
import json


class KnowledgeGraph:
    """
    Graph-based subject dependency system
    Models how failure in prerequisites affects future courses
    """
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self._initialize_default_graph()
    
    def _initialize_default_graph(self):
        """
        Initialize with common prerequisite relationships
        In production, this would be loaded from institutional data
        """
        # Define subjects and their prerequisites
        dependencies = [
            # Mathematics track
            ('Calculus I', 'Calculus II', 0.9),
            ('Calculus II', 'Calculus III', 0.85),
            ('Calculus I', 'Linear Algebra', 0.7),
            ('Linear Algebra', 'Differential Equations', 0.8),
            
            # Programming track
            ('Programming Fundamentals', 'Data Structures', 0.95),
            ('Data Structures', 'Algorithms', 0.90),
            ('Programming Fundamentals', 'Object Oriented Programming', 0.85),
            ('Data Structures', 'Database Systems', 0.70),
            
            # Physics track
            ('Physics I', 'Physics II', 0.85),
            ('Calculus I', 'Physics I', 0.75),
            ('Physics II', 'Quantum Mechanics', 0.80),
            
            # Core to advanced
            ('Calculus I', 'Probability and Statistics', 0.70),
            ('Programming Fundamentals', 'Machine Learning', 0.80),
            ('Linear Algebra', 'Machine Learning', 0.85),
            ('Algorithms', 'Advanced Algorithms', 0.90),
            
            # Engineering track
            ('Chemistry', 'Organic Chemistry', 0.85),
            ('Physics I', 'Thermodynamics', 0.75),
            ('Calculus II', 'Engineering Mathematics', 0.80),
        ]
        
        # Add edges with dependency strength
        for prereq, course, strength in dependencies:
            self.graph.add_edge(prereq, course, strength=strength)
            
            # Add node attributes
            if prereq not in self.graph.nodes:
                self.graph.add_node(prereq, difficulty=0.75)
            if course not in self.graph.nodes:
                self.graph.add_node(course, difficulty=0.75)
    
    def add_dependency(self, prerequisite: str, course: str, strength: float):
        """Add a new prerequisite relationship"""
        self.graph.add_edge(prerequisite, course, strength=strength)
    
    def get_prerequisites(self, course: str) -> List[Dict[str, Any]]:
        """
        Get all prerequisites for a course with dependency strength
        """
        if course not in self.graph:
            return []
        
        prerequisites = []
        for prereq in self.graph.predecessors(course):
            strength = self.graph[prereq][course]['strength']
            prerequisites.append({
                'subject': prereq,
                'dependency_strength': strength
            })
        
        return sorted(prerequisites, key=lambda x: x['dependency_strength'], reverse=True)
    
    def get_dependent_courses(self, course: str) -> List[Dict[str, Any]]:
        """
        Get all courses that depend on this course
        """
        if course not in self.graph:
            return []
        
        dependents = []
        for dependent in self.graph.successors(course):
            strength = self.graph[course][dependent]['strength']
            dependents.append({
                'subject': dependent,
                'dependency_strength': strength
            })
        
        return sorted(dependents, key=lambda x: x['dependency_strength'], reverse=True)
    
    def calculate_dependency_depth(self, course: str) -> int:
        """
        Calculate how many prerequisite levels deep a course is
        Higher depth = more foundational knowledge required
        """
        if course not in self.graph:
            return 0
        
        try:
            # Find longest path to this course
            paths = []
            for node in self.graph.nodes:
                if node != course and nx.has_path(self.graph, node, course):
                    try:
                        path_length = nx.shortest_path_length(self.graph, node, course)
                        paths.append(path_length)
                    except nx.NetworkXNoPath:
                        continue
            
            return max(paths) if paths else 0
        except:
            return 0
    
    def propagate_risk(self, failed_course: str, failure_risk: float) -> Dict[str, float]:
        """
        Propagate failure risk forward to dependent courses
        
        Args:
            failed_course: Course where student is at risk
            failure_risk: Probability of failure in that course
        
        Returns:
            Dictionary mapping future courses to propagated risk
        """
        if failed_course not in self.graph:
            return {}
        
        propagated_risks = {}
        
        # BFS to propagate risk through graph
        visited = set()
        queue = [(failed_course, failure_risk)]
        
        while queue:
            current_course, current_risk = queue.pop(0)
            
            if current_course in visited:
                continue
            visited.add(current_course)
            
            # Propagate to dependent courses
            for dependent in self.graph.successors(current_course):
                edge_strength = self.graph[current_course][dependent]['strength']
                
                # Risk decays with dependency strength
                propagated_risk = current_risk * edge_strength * 0.8  # 0.8 decay factor
                
                # Accumulate risk if multiple prerequisites at risk
                if dependent in propagated_risks:
                    # Take maximum risk (pessimistic assumption)
                    propagated_risks[dependent] = max(propagated_risks[dependent], propagated_risk)
                else:
                    propagated_risks[dependent] = propagated_risk
                
                # Continue propagation if risk is significant
                if propagated_risk > 0.2:
                    queue.append((dependent, propagated_risk))
        
        # Remove the source course from results
        propagated_risks.pop(failed_course, None)
        
        return propagated_risks
    
    def get_critical_prerequisites(self, current_courses: List[str]) -> List[Dict[str, Any]]:
        """
        Identify prerequisite courses that are critical for current enrollment
        
        Returns courses that are prerequisites for multiple current courses
        """
        prerequisite_counts = {}
        
        for course in current_courses:
            prereqs = self.get_prerequisites(course)
            for prereq in prereqs:
                prereq_name = prereq['subject']
                if prereq_name not in prerequisite_counts:
                    prerequisite_counts[prereq_name] = {
                        'subject': prereq_name,
                        'dependent_courses': [],
                        'avg_strength': 0.0,
                        'criticality': 0
                    }
                
                prerequisite_counts[prereq_name]['dependent_courses'].append(course)
        
        # Calculate criticality
        critical_prereqs = []
        for prereq_name, info in prerequisite_counts.items():
            num_dependents = len(info['dependent_courses'])
            
            # Calculate average dependency strength
            strengths = []
            for course in info['dependent_courses']:
                if self.graph.has_edge(prereq_name, course):
                    strengths.append(self.graph[prereq_name][course]['strength'])
            
            avg_strength = sum(strengths) / len(strengths) if strengths else 0
            
            # Criticality = number of dependents × average strength
            criticality = num_dependents * avg_strength
            
            info['avg_strength'] = round(avg_strength, 3)
            info['criticality'] = round(criticality, 3)
            
            critical_prereqs.append(info)
        
        # Sort by criticality
        return sorted(critical_prereqs, key=lambda x: x['criticality'], reverse=True)
    
    def get_learning_path(self, target_course: str) -> List[str]:
        """
        Get recommended learning path (topological order) to reach target course
        """
        if target_course not in self.graph:
            return [target_course]
        
        # Get all prerequisites
        try:
            ancestors = nx.ancestors(self.graph, target_course)
            subgraph = self.graph.subgraph(list(ancestors) + [target_course])
            
            # Topological sort gives learning order
            path = list(nx.topological_sort(subgraph))
            return path
        except:
            return [target_course]
    
    def export_graph(self) -> Dict[str, Any]:
        """Export graph structure for visualization"""
        return {
            'nodes': [
                {
                    'id': node,
                    'difficulty': self.graph.nodes[node].get('difficulty', 0.75)
                }
                for node in self.graph.nodes
            ],
            'edges': [
                {
                    'source': u,
                    'target': v,
                    'strength': self.graph[u][v]['strength']
                }
                for u, v in self.graph.edges
            ]
        }
