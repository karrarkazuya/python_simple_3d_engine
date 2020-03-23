

class Maths:
    def __init__(self):
        super().__init__()

    def area_of_poly(self, A, B, C):
        y1 = B[1] - C[1]
        y2 = C[1] - A[1]
        y3 = A[1] - B[1]
        return abs((A[0] * y1 + B[0] * y2 + C[0] * y3) / 2.0)

    def sign_of_poly(self, A, B, C):
        return (A[0] - C[0]) * (B[1] - C[1]) - (B[0] - C[0]) * (A[1] - C[1])

    def point_in_poly(self, point, poly):
        total_area = self.area_of_poly(poly[0], poly[1], poly[2])
        area1 = self.area_of_poly(point, poly[0], poly[1])
        area2 = self.area_of_poly(point, poly[1], poly[2])
        area3 = self.area_of_poly(point, poly[2], poly[0])

        return (area1 + area2 + area3) == total_area

    def poly_inside_poly(self, poly1, poly2):
        A = self.point_in_poly(poly1[0], poly2)
        B = self.point_in_poly(poly2[1], poly2)
        C = self.point_in_poly(poly2[2], poly2)
        return A and B and C
