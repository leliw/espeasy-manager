import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';

export interface Node {
    ip: string;
    name: string;
    unit_no: number;
}
@Component({
    selector: 'app-root',
    standalone: true,
    imports: [CommonModule, RouterOutlet, HttpClientModule],
    templateUrl: './app.component.html',
    styleUrl: './app.component.css'
})
export class AppComponent {

    nodes: Node[] = [];

    constructor(private http: HttpClient) {
        http.get<Node[]>('/api/nodes').subscribe(data => {
            this.nodes = data;
            console.log(data);
        });
    }

}
