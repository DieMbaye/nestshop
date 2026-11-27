import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Product {
  id: number;
  name: string;
  description: string | null;
  price: number;
  stock: number;
}

export interface OrderCreate {
  customer_name: string;
  product_id: number;
  quantity: number;
}

export interface Order {
  id: number;
  customer_name: string;
  product_id: number;
  quantity: number;
  total: number;
  created_at: string;
}

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);

  getProducts(): Observable<Product[]> {
    return this.http.get<Product[]>('/api/products');
  }

  createOrder(order: OrderCreate): Observable<Order> {
    return this.http.post<Order>('/api/orders', order);
  }
}