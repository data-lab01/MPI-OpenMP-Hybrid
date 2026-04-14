// Comprehensive help system for all TransForgeX1 pages

const HelpLibrary = {
    // Scaling Laws
    amdahl: {
        title: "Amdahl's Law",
        content: `<h4>📐 Amdahl's Law (1967)</h4>
        <p><strong>Formula:</strong> Speedup = 1 / (S + (1-S)/N)</p>
        <p><strong>Where:</strong> S = serial fraction, N = number of processors</p>
        <p><strong>Key Insight:</strong> The serial portion of your code limits maximum speedup, no matter how many cores you add.</p>
        <p><strong>Example:</strong> If 10% is serial, max speedup is 10x even with 1000 cores.</p>
        <p><strong>Application:</strong> Used to estimate parallel performance bounds.</p>`
    },
    gustafson: {
        title: "Gustafson's Law",
        content: `<h4>📈 Gustafson's Law (1988)</h4>
        <p><strong>Formula:</strong> Speedup = N - S×(N-1)</p>
        <p><strong>Key Insight:</strong> With larger problem sizes, speedup scales almost linearly.</p>
        <p><strong>Why it matters:</strong> More realistic for modern HPC where problem size grows with available cores.</p>`
    },
    
    // Scheduling
    fifo: {
        title: "FIFO Scheduling",
        content: `<h4>🔄 First-In-First-Out</h4>
        <p><strong>How it works:</strong> Jobs execute in arrival order.</p>
        <p><strong>Pros:</strong> Simple, fair, no starvation</p>
        <p><strong>Cons:</strong> Convoy effect - short jobs wait behind long jobs</p>
        <p><strong>Used in:</strong> Batch systems, simple queues</p>`
    },
    backfill: {
        title: "EASY-Backfill",
        content: `<h4>🔄 Backfill Scheduling</h4>
        <p><strong>How it works:</strong> Small jobs can jump ahead if they don't delay the first large job.</p>
        <p><strong>Benefits:</strong> 20-40% better utilization than FIFO</p>
        <p><strong>Used in:</strong> Slurm, PBS, LSF (production schedulers)</p>`
    },
    priority: {
        title: "Priority Scheduling",
        content: `<h4>⭐ Priority Scheduling</h4>
        <p><strong>How it works:</strong> Jobs with higher priority execute first.</p>
        <p><strong>Formula:</strong> Priority = 1 / nodes_requested (smaller jobs get higher priority)</p>
        <p><strong>Benefit:</strong> Reduces fragmentation for mixed workloads</p>`
    },
    
    // Network
    fat_tree: {
        title: "Fat Tree Topology",
        content: `<h4>🌳 Fat Tree Network</h4>
        <p><strong>Properties:</strong> Full bisection bandwidth, O(log N) diameter</p>
        <p><strong>Used in:</strong> Many HPC clusters, data centers</p>
        <p><strong>Advantage:</strong> No bandwidth bottlenecks</p>`
    },
    dragonfly: {
        title: "Dragonfly Topology",
        content: `<h4>🐉 Dragonfly Network</h4>
        <p><strong>Properties:</strong> 3-hop routing, diameter of 3</p>
        <p><strong>Used in:</strong> Cray supercomputers (Frontier, LUMI)</p>
        <p><strong>Advantage:</strong> Excellent scalability to exascale</p>`
    },
    torus: {
        title: "Torus Topology",
        content: `<h4>🔄 Torus Network</h4>
        <p><strong>Properties:</strong> Regular structure, wrap-around connections</p>
        <p><strong>Used in:</strong> IBM Blue Gene, some Japanese supercomputers</p>
        <p><strong>Best for:</strong> Stencil computations, regular communication patterns</p>`
    },
    
    // GPU
    memory_bound: {
        title: "Memory Bound Workload",
        content: `<h4>💾 Memory-Bound Workloads</h4>
        <p><strong>Characteristics:</strong> Low compute/memory ratio, many memory accesses</p>
        <p><strong>Optimization:</strong> Use shared memory, reduce global memory accesses</p>
        <p><strong>Example:</strong> Sparse matrix operations, graph algorithms</p>`
    },
    compute_bound: {
        title: "Compute Bound Workload",
        content: `<h4>⚡ Compute-Bound Workloads</h4>
        <p><strong>Characteristics:</strong> High compute/memory ratio, many floating-point operations</p>
        <p><strong>Optimization:</strong> Increase occupancy, reduce thread divergence</p>
        <p><strong>Example:</strong> Matrix multiplication, FFT, dense linear algebra</p>`
    },
    
    // MPI
    mpi_bcast: {
        title: "MPI_Bcast",
        content: `<h4>📡 MPI_Bcast (Broadcast)</h4>
        <p><strong>Purpose:</strong> One process sends same data to all others</p>
        <p><strong>Algorithm:</strong> Tree-based (binomial tree)</p>
        <p><strong>Complexity:</strong> O(log P) steps</p>
        <p><strong>Use case:</strong> Distributing input data, configuration parameters</p>`
    },
    mpi_reduce: {
        title: "MPI_Reduce",
        content: `<h4>📡 MPI_Reduce</h4>
        <p><strong>Purpose:</strong> Combines values from all processes (sum, max, min, etc.)</p>
        <p><strong>Algorithm:</strong> Tree-based reduction</p>
        <p><strong>Complexity:</strong> O(log P) steps</p>
        <p><strong>Use case:</strong> Global statistics, convergence checks</p>`
    },
    mpi_allreduce: {
        title: "MPI_Allreduce",
        content: `<h4>📡 MPI_Allreduce</h4>
        <p><strong>Purpose:</strong> Reduce + Broadcast combined - all processes get result</p>
        <p><strong>Algorithm:</strong> Recursive doubling</p>
        <p><strong>Complexity:</strong> O(log P) steps</p>
        <p><strong>Use case:</strong> Gradient averaging in distributed ML</p>`
    },
    
    // OpenMP
    omp_static: {
        title: "Static Schedule",
        content: `<h4>📋 OpenMP Static Schedule</h4>
        <p><strong>How it works:</strong> Iterations divided equally at compile time</p>
        <p><strong>Best for:</strong> Regular workloads with uniform iteration costs</p>
        <p><strong>Overhead:</strong> Very low</p>
        <p><strong>Example:</strong> Dense matrix operations</p>`
    },
    omp_dynamic: {
        title: "Dynamic Schedule",
        content: `<h4>📋 OpenMP Dynamic Schedule</h4>
        <p><strong>How it works:</strong> Threads grab iterations at runtime</p>
        <p><strong>Best for:</strong> Irregular workloads, load imbalance</p>
        <p><strong>Overhead:</strong> Higher than static</p>
        <p><strong>Example:</strong> Sparse computations, adaptive algorithms</p>`
    },
    omp_guided: {
        title: "Guided Schedule",
        content: `<h4>📋 OpenMP Guided Schedule</h4>
        <p><strong>How it works:</strong> Starts with large chunks, decreases dynamically</p>
        <p><strong>Best for:</strong> Balancing overhead and load imbalance</p>
        <p><strong>Advantage:</strong> Good default choice</p>`
    },
    
    // European Standards
    eurohpc: {
        title: "EuroHPC JU",
        content: `<h4>🇪🇺 European High-Performance Computing Joint Undertaking</h4>
        <p><strong>Purpose:</strong> Develop world-class exascale supercomputing in Europe</p>
        <p><strong>Systems:</strong> LUMI (Finland), Leonardo (Italy), MareNostrum5 (Spain)</p>
        <p><strong>Requirements:</strong> PUE < 1.2, renewable energy, EPI processors</p>`
    },
    prace: {
        title: "PRACE",
        content: `<h4>📊 Partnership for Advanced Computing in Europe</h4>
        <p><strong>Purpose:</strong> Provide world-class HPC resources for European researchers</p>
        <p><strong>Benchmarks:</strong> HPL, HPCG, IO500, Graph500</p>
        <p><strong>Ratings:</strong> Gold (>80%), Silver (>60%), Bronze</p>`
    },
    gaiax: {
        title: "GAIA-X",
        content: `<h4>🔒 GAIA-X Data Infrastructure</h4>
        <p><strong>Purpose:</strong> European sovereign data infrastructure</p>
        <p><strong>Requirements:</strong> Data sovereignty, GDPR compliance, interoperability</p>
        <p><strong>Standards:</strong> IDS, EDC, SSI</p>`
    }
};

// Helper function to show help popup
function showHelp(topic) {
    const help = HelpLibrary[topic];
    if (help) {
        ExplanationPopup.show(help.title, help.content);
    } else {
        ExplanationPopup.show("Information", "Detailed help content will appear here.");
    }
}

// Add help icons to elements
function addHelpToElement(elementId, topic) {
    const element = document.getElementById(elementId);
    if (element) {
        const helpIcon = document.createElement('span');
        helpIcon.className = 'explanation-icon';
        helpIcon.innerHTML = '?';
        helpIcon.style.marginLeft = '8px';
        helpIcon.onclick = (e) => {
            e.stopPropagation();
            showHelp(topic);
        };
        element.parentElement?.insertBefore(helpIcon, element.nextSibling);
    }
}

// Initialize help icons on page load
document.addEventListener('DOMContentLoaded', () => {
    // Add help icons to section titles
    const sections = [
        { id: 'scalingTitle', topic: 'amdahl' },
        { id: 'schedulingTitle', topic: 'fifo' },
        { id: 'networkTitle', topic: 'fat_tree' },
        { id: 'mpiTitle', topic: 'mpi_bcast' },
        { id: 'openmpTitle', topic: 'omp_static' }
    ];
    
    sections.forEach(section => {
        addHelpToElement(section.id, section.topic);
    });
});
