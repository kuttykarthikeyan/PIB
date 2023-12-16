# from celery import shared_task
# # import os,fitz 
# from ultralytics import YOLO
# import cv2

# model = YOLO(r"model_ocr\best_model_article.pt")
# classes_list = model.names


# @shared_task
# def perform_ocr():
#     detected_object_name_list = [] 

#     files_name_folder = [f for f in os.listdir("pdfs") if os.path.isfile(os.path.join("pdfs", f))]

#     for file_name in files_name_folder[0:2]:
            
#         doc = fitz.open("pdfs/"+file_name)
#         os.makedirs("OCR_results/" + file_name + "_pdf", exist_ok=True)

#         for id, page in enumerate(doc):
#             pix = page.get_pixmap(matrix=fitz.Identity, dpi=None, colorspace=fitz.csRGB, clip=None, annots=True)
#             pix.save("images_from_pdf/samplepdfimage-%i.jpg" % page.number)
#             input_image = cv2.imread("images_from_pdf/samplepdfimage-%i.jpg" % page.number)

#             results = model.predict(source="images_from_pdf/samplepdfimage-%i.jpg" % page.number, conf=0.20,iou=0.8)
#             results_image = results[0].plot()
            
#             os.makedirs("OCR_results/" + file_name + "_pdf" + "/page_"+str(id+1),exist_ok=True)

#             cv2.imwrite("OCR_results/" + file_name + "_pdf" + "/page_"+str(id+1)+"/full_image.jpg", results_image)

#             boxes = results[0].boxes.numpy().xyxy
#             classes = results[0].boxes.numpy().cls
#             img_num = 1
#             for b, c in zip(boxes, classes):
#                 if c == 0:
#                     x1, y1 = b[0], b[1]  # Top-left corner
#                     x2, y2 = b[2], b[3]  # Bottom-right corner
#                     x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
#                     cropped_image = input_image[y1:y2, x1:x2]

#                     cv2.imwrite("OCR_results/" + file_name + "_pdf" + "/page_"+str(id+1)+"/article_" + str(img_num) + ".png", cropped_image)
#                     img_num += 1
#             img_num = 1
