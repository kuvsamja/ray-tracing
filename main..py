import math
import sys
image_width = 400
aspect_ratio = 4 / 3
image_height = int(image_width // aspect_ratio)

def main():
    with open("img.ppm", "w") as f:
        f.write(f"P3\n{image_width} {image_height}\n255\n")
        
        for j in range(image_height):
            for i in range(image_width):
                sys.stdout.write(f"{i} {j} \n")
                r = i / (image_width - 1)
                g = j / (image_height - 1)
                b = 0.0

                ir = int(255 * r)
                ig = int(255 * g)
                ib = int(255 * b)
            
                f.write(f"{str(ir)} {str(ig)} {str(ib)}\n")
    print("done")
if __name__ == "__main__":
    main()