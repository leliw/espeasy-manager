import { Component, OnInit } from '@angular/core';
import { NodeHeader, NodesService } from '../nodes.service';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
    selector: 'app-nodes-table',
    standalone: true,
    imports: [CommonModule, RouterModule],
    templateUrl: './nodes-table.component.html',
    styleUrl: './nodes-table.component.css'
})
export class NodesTableComponent implements OnInit {

    nodes!: NodeHeader[];

    constructor(private nodeService: NodesService) { }

    ngOnInit() {
        this.nodeService.getNodes().subscribe(nodes => {
            this.nodes = nodes;
        });
    }

}
