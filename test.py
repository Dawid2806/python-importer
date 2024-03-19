import json
import csv

def transform_and_export_orders(old_orders_file, new_orders_csv_file, images_csv_file, new_orders_sql_file, images_sql_file, base_image_url):
    with open(old_orders_file, 'r', encoding='utf-8') as file:
        old_orders_data = json.load(file)

    new_orders = []
    order_images = []
    order_id_counter = 1  # Inicjowanie licznika ID

    for order in old_orders_data:
        if order['status'] == 6:
            continue

        service_id = str(order['cleaning_id']) if order['cleaning_id'] is not None else None
        if order['renovations_id'] is not None:
            service_id = str(int(order['renovations_id']) + 5)

        order_type_map = {6: 1, 7: 2}
        order_type_id = order_type_map.get(order['ordersTyps'], None)

        new_order = {
            "id": order_id_counter,
            "phone": order["phone"],
            "size": order["size"],
            "color": order["color"],
            "brand": order["brand"],
            "orderNumber": order["order_number"],
            "created_at": order["date_of_reception"],
            "service_id": service_id,
            "due_date": order['due_date'],
            "comment": order['comment'],
            "additional_service_id": '1',
            "reasonForDelay": order['reasonfordelay'],
            "shipping_number": order["shippingNumber"],
            "order_type_id": order_type_id,
            'order_status_id': order["status"]
        }
        new_orders.append(new_order)
        order_id_counter += 1  # Inkrementacja licznika ID po każdym dodaniu zamówienia

        for img_field in ['img_one', 'img_two', 'img_thee', 'img_four', 'img_five', 'img_six', 'img_seven', 'img_eight']:
            img_id = order.get(img_field)
            if img_id:
                image_url = f"{base_image_url}{img_id}"
                order_images.append({
                    "order_id": order_id_counter,
                    "image": image_url,
                    "status": "active"
                })

    # Zapis do CSV
    with open(new_orders_csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=new_orders[0].keys())
        writer.writeheader()
        writer.writerows(new_orders)

    with open(images_csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=order_images[0].keys())
        writer.writeheader()
        writer.writerows(order_images)

    def escape_single_quotes(value):
        return str(value).replace("'", "''")

    with open(new_orders_sql_file, 'w', encoding='utf-8') as file:
        for order in new_orders:
            columns = ', '.join(order.keys())
            values = ', '.join([f"'{escape_single_quotes(value)}'" for value in order.values()])
            sql = f"INSERT INTO public_python_order ({columns}) VALUES ({values});\n"
            file.write(sql)

    with open(images_sql_file, 'w', encoding='utf-8') as file:
        for image in order_images:
            columns = ', '.join(image.keys())
            values = ', '.join([f"'{escape_single_quotes(value)}'" for value in image.values()])
            sql = f"INSERT INTO order_images ({columns}) VALUES ({values});\n"
            file.write(sql)

# Przykładowe wywołanie funkcji
transform_and_export_orders(
    'orderss.json',
    'orders-new.csv',
    'order-images.csv',
    'orders-new.sql',
    'order-images.sql',
    'https://wcxfnjdgopvlgyaxkdaw.storage.eu-central-1.nhost.run/v1/files/'
)
