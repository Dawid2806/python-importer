import json

def transform_orders(old_orders_file, new_orders_file, images_file, base_image_url):
    with open(old_orders_file, 'r', encoding='utf-8') as file:
        old_orders_data = json.load(file)

    new_orders = []
    order_images = []  # Inicjowanie poza pętlą for

    for order in old_orders_data:
        if order['status'] == 6:  # Pomijanie zamówień ze statusem 6
            continue

        # Przypisanie service_id na podstawie cleaning_id i renovations_id
        service_id = str(order['cleaning_id']) if order['cleaning_id'] is not None else None
        if order['renovations_id'] is not None:
            service_id = str(int(order['renovations_id']) + 5)

        # Mapowanie ordersTyps do order_type_id
        order_type_map = {6: 1, 7: 2}
        order_type_id = order_type_map.get(order['ordersTyps'], None)

        new_order = {
            "id": order["id"],
            "phone": order["phone"],
            "size": order["size"],
            "color": order["color"],
            "brand": order["brand"],
            "orderNumber": order["order_number"],
            "created_at": order["date_of_reception"],
            "service_id": service_id,
            "due_date": order['due_date'],
            "comment": order['comment'],
            "additional_service_id": order["addtives_id"],
            "reasonForDelay": order['reasonfordelay'],
            "shipping_number": order["shippingNumber"],
            "order_type_id": order_type_id,
            'order_status_id': order["status"]
        }
        new_orders.append(new_order)

        # Dodawanie obrazów dla każdego zamówienia
        for img_field in ['img_one', 'img_two', 'img_thee', 'img_four', 'img_five', 'img_six', 'img_seven', 'img_eight']:
            img_id = order.get(img_field)
            if img_id:
                image_url = f"{base_image_url}{img_id}"
                order_images.append({
                    "order_id": order["id"],
                    "image": image_url,
                    "status": "active"
                })

    # Zapis obrazów zamówień do osobnego pliku
    with open(images_file, 'w', encoding='utf-8') as file:
        json.dump(order_images, file, ensure_ascii=False, indent=4)

    # Zapis nowych danych zamówień do pliku
    with open(new_orders_file, 'w', encoding='utf-8') as file:
        json.dump(new_orders, file, ensure_ascii=False, indent=4)

# Przykładowe wywołanie funkcji
transform_orders('orderss.json', 'orders-new.json', 'order-images.json', 'https://wcxfnjdgopvlgyaxkdaw.storage.eu-central-1.nhost.run/v1/files/')
