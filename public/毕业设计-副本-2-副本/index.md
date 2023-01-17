# 毕业设计

# 操作系统实验

## 实验三

### 生产者线程函数和消费者线程函数中的临界资源是什么?

临界资源只有一个，即存储产品的缓冲池。具体代码如下：

```c
//
// 缓冲池。
//
#define BUFFER_SIZE		10
int Buffer[BUFFER_SIZE];
```

### 生产者线程函数和消费者线程函数中分别有哪些代码是临界区?

```c
//
// 生产者线程函数。
//
ULONG Producer(PVOID Param) 
{
	int i;
	int InIndex = 0;

	for (i = 0; i < PRODUCT_COUNT; i++) {

		WaitForSingleObject(EmptySemaphoreHandle, INFINITE);
		WaitForSingleObject(MutexHandle, INFINITE);
		
// ============================临界区==============================
		printf("Produce a %d\n", i);
		Buffer[InIndex] = i;
		InIndex = (InIndex + 1) % BUFFER_SIZE;
// ===============================================================
		ReleaseMutex(MutexHandle);
		ReleaseSemaphore(FullSemaphoreHandle, 1, NULL);

		//
		// 休息一会。每 500 毫秒生产一个数。
		//
		Sleep(500);
	}
	
	return 0;
}
```

```c
//
// 消费者线程函数。
//
ULONG Consumer(PVOID Param)
{
    int i;
    int OutIndex = 0;

    for (i = 0; i < PRODUCT_COUNT; i++) {

        WaitForSingleObject(FullSemaphoreHandle, INFINITE);
        WaitForSingleObject(MutexHandle, INFINITE);
// ========================临界区==================================
        printf("\t\t\tConsume a %d\n", Buffer[OutIndex]);
        OutIndex = (OutIndex + 1) % BUFFER_SIZE;
// ===============================================================
        ReleaseMutex(MutexHandle);
        ReleaseSemaphore(EmptySemaphoreHandle, 1, NULL);

        //
        // 休息一会儿。让前 10 个数的消费速度比较慢，后面的较快。
        //
        if (i < 10) {
            Sleep(2000);
        } else {
            Sleep(100);
        }
}
```

### 生产者线程函数和消费者线程函数中进入临界区和退出临界区的代码是哪些?是否成对出现?

```c
//
// 生产者线程函数。
//
ULONG Producer(PVOID Param) 
{
	int i;
	int InIndex = 0;

	for (i = 0; i < PRODUCT_COUNT; i++) {
// ==========================进入临界区的代码====================
		WaitForSingleObject(EmptySemaphoreHandle, INFINITE);
		WaitForSingleObject(MutexHandle, INFINITE);
// ===========================================================
		printf("Produce a %d\n", i);
		Buffer[InIndex] = i;
		InIndex = (InIndex + 1) % BUFFER_SIZE;
// ==========================退出临界区的代码====================
		ReleaseMutex(MutexHandle);
		ReleaseSemaphore(FullSemaphoreHandle, 1, NULL);
// ===========================================================
		//
		// 休息一会。每 500 毫秒生产一个数。
		//
		Sleep(500);
	}
	
	return 0;
}
```

```c
//
// 消费者线程函数。
//
ULONG Consumer(PVOID Param)
{
	int i;
	int OutIndex = 0;

	for (i = 0; i < PRODUCT_COUNT; i++) {
// ==========================进入临界区的代码====================
		WaitForSingleObject(FullSemaphoreHandle, INFINITE);
		WaitForSingleObject(MutexHandle, INFINITE);
// ===========================================================
		printf("\t\t\tConsume a %d\n", Buffer[OutIndex]);
		OutIndex = (OutIndex + 1) % BUFFER_SIZE;
// ==========================退出临界区的代码====================
		ReleaseMutex(MutexHandle);
		ReleaseSemaphore(EmptySemaphoreHandle, 1, NULL);
// ===========================================================
		//
		// 休息一会儿。让前 10 个数的消费速度比较慢，后面的较快。
		//
		if (i < 10) {
			Sleep(2000);
		} else {
			Sleep(100);
		}
	}
	
	return 0;
}
```

### 生产者线程和消费者线程是如何使用 Mutex、Empty 信号量和 Full 信号量来实现同步的?这两个线程函数中对这三个同步对象的操作能够改变顺序吗?

**不能改变顺序**

在生产者和消费者问题中，`Mutex`信号量是互斥信号量，确保生产者和消费者对缓冲区资源的互斥访问。Empty和Full信号量是资源信号量，`Empty`代表缓冲区中的空闲空间，`Full`代表缓冲区中的产品数量，Empty和Full用来处理生产者和消费者之间的同步问题。

如果将生产者和消费者中的两次wait操作次序进行修改，则可能会发生死锁。可以考虑如下场景：

将Mutex和 Full 信号量位置交换。当缓冲区空间已满时，这个时候生产者执行wait(mutex), wait(empty)操作尝试向缓冲区中放置产品，那么因为没有空闲资源该生产者进入等待状态。而其他的生产者和消费者在这个时候又无法获取mutex信号量使用临界区，此时就会发生死锁。如果将生产者和消费者的两次release操作次序进行修改则不会发生死锁，只是资源的释放时机发生了改变。

其他交换情况也会发生死锁和不符合生产者-消费者模型的异常，因此三种信号量的位置不能交换。

## 实验四

### 使用“关中断”和“开中断”保护临界资源的原因

一般得临界资源在进程同步只需要使用信号量机制解决，但有些在内核态执行的系统函数则需要使用中断机制解决同步问题，下面以EOS的线程调度函数`ThreadFunction`为例说明:

首先，中断机制可以和信号量一样实现对临界资源的互斥访问。当关闭中断后CPU就不会响应任何由外部设备发出的硬中断（包括定时计数器中断和键盘中断等）了，也就不会发生线程调度了，从而保证各个线程可以互斥的访问控制台。

其次，这里绝对不能使用互斥信号量`（Mutex）`保护临界资源的原因：如果使用互斥信号量，则那些由于访问临界区而被阻塞的线程，就会被放入互斥信号量的等待队列，就不会在相应优先级的就绪列中了。使用“关中断”和“开中断”进行同步就不会改变线程的状态，可以保证那些没有获得处理器的线程都在处于就绪队列中。从而使得调度函数正常执行。

### 使低优先级线程也能获得执行机会的调度算法在 ke/sysprocc 文件中的 ConsoleCmdRoundRobin 函数调用 Sleep 函数语句的后面添加下面的语句，即可以演示高优先级线程抢占处理器后，低优先级线程无法运行的情况，待高优先级线程结束后，低优先级线程才能够继续运行。

```c
HANDLE ThreadHandle;
THREAD PARAMETER ThreadParameter.
asm("cli")
ThreadParameter.Y = 20:
ThreadParameter.StdHandle = StdHandle
ThreadHandle =(HANDLE)CreateThread(
0, ThreadFunction,(PVOID)&ThreadParameter, 0, NULL):
PsSetThreadPriority(ThreadHandle,9):
asm("sti"):
Sleep(101000):
TerminateThread(ThreadHandle, 0):
CloseHandle(ThreadHandle);
Sleep(101000);
```

### Windows、Linux 中的时间片轮转调度 在 Windows、Linux 等操作系统中，虽然都提供了时间片轮转调度算法，但时间片轮转 调度算法却很少真正被派上用场，下面解释原因。

在Windows、linux等操作系统中，虽然都提供了时间片轮转调度算法却很少真正被派上用场，原因如下。

在Windows任务管理器中，即使系统中已经运行了数百个线程，但CPU的利用率仍然很低，甚至为0，因为这些线程在大部分时间都处于阻塞状态。阻塞的原因是各种各样的，最主要的原因是等待I/O完成或者等待命令消息的到达。

例如，在编辑Word文档时，每敲击一次键盘，Word就会立即作出反应，并且文档中插入字符。此时会感觉Word运行的非常流畅。事实上，并非如此，Word主线程大部分时间都处于阻塞等待状态，等待用户敲击键盘。在用户没有敲击键盘或没有使用鼠标点击时，Word主线程处于阻塞状态，它将让出处理器给其它需要的线程。当用户敲击一个按键后，Word主线程将会立刻被操作系统唤醒，此时Word开始处理请求。Word在处理输入请求时所用的CPU时间是非常短的，是微秒级的，远远低于时间片轮转调度的时间片大小，处理完毕后Word又立刻进入阻塞状态，等待用户下一次敲击键盘。

从上述的例子可以看出，如果按照时间片轮转算法，那么必将有很多的时间片浪费给

## 实验五

### 在应用程序进程中分配虚拟页和释放虚拟页的源代码。

```c
PRIVATE
VOID
ConsoleCmdVM(
	IN HANDLE StdHandle,
	IN PCSTR Arg
	)
{
	BOOL IntState;
	ULONG ProcID;
	PPROCESS pProcCtrlBlock;
	PMMVAD_LIST pVadList;
	PLIST_ENTRY pListEntry;
	PMMVAD pVad;
	ULONG Index, TotalVpnCount, AllocatedVpnCount, FreeVpnCount, VpnCount;
	STATUS Status;
	
	const char* OutputFormat = NULL;
	
	//
	// 从命令参数字符串中获得进程 ID。
	//
	ProcID = atoi(Arg);
	if(0 == ProcID) {
		fprintf(StdHandle, "Please input a valid process ID.\n");
		return;
	}
	
	//
	// 由进程 ID 获得进程控制块
	//
	Status = ObRefObjectById(ProcID, PspProcessType, (PVOID*)&pProcCtrlBlock);
	if (!EOS_SUCCESS(Status)) {
		fprintf(StdHandle, "%d is an invalid process ID.\n", ProcID);
		return;
	}
	
	IntState = KeEnableInterrupts(FALSE);	// 关中断
	
	//
	// 将进程控制块中 VAD 链表的指针保存下来，方便后面使用
	//
	pVadList = &pProcCtrlBlock->Pas->VadList;
	
	//
	// 输出 VAD 链表中记录的起始页框号，结束页框号
	//
	OutputFormat = "Total Vpn from %d to %d. (0x%X - 0x%X)\n\n";
	fprintf(StdHandle, OutputFormat,
		pVadList->StartingVpn, pVadList->EndVpn,
		pVadList->StartingVpn * PAGE_SIZE, (pVadList->EndVpn + 1) * PAGE_SIZE - 1);
	
	//
	// 遍历 VAD 链表，输出所有 VAD 的起始页框号，结束页框号和包含的虚拟页框数量
	//
	Index = AllocatedVpnCount = 0;
	for(pListEntry = pVadList->VadListHead.Next;
		pListEntry != &pVadList->VadListHead;
		pListEntry = pListEntry->Next) {
	
		Index++;
		pVad = CONTAINING_RECORD(pListEntry, MMVAD, VadListEntry);
		
		VpnCount = pVad->EndVpn - pVad->StartingVpn + 1;
		OutputFormat = "%d# Vad Include %d Vpn From %d to %d. (0x%X - 0x%X)\n";
		fprintf(StdHandle, OutputFormat,
			Index, VpnCount, pVad->StartingVpn, pVad->EndVpn,
			pVad->StartingVpn * PAGE_SIZE, (pVad->EndVpn + 1) * PAGE_SIZE - 1);
		
		AllocatedVpnCount += VpnCount;
	}
	
	//
	// 统计虚拟页框总数、已分配的虚拟页框和未分配的虚拟页框
	//
	TotalVpnCount = pVadList->EndVpn - pVadList->StartingVpn + 1;
	OutputFormat = "\nTotal Vpn Count: %d.\n";
	fprintf(StdHandle, OutputFormat, TotalVpnCount);
	
	OutputFormat = "Allocated Vpn Count: %d.\n";
	fprintf(StdHandle, OutputFormat, AllocatedVpnCount);
	
	FreeVpnCount = TotalVpnCount - AllocatedVpnCount;
	OutputFormat = "Free Vpn Count: %d.\n\n";
	fprintf(StdHandle, OutputFormat, FreeVpnCount);
	
	//
	// 输出物理页的零页数量和空闲页数量
	//
	OutputFormat = "Zeroed Physical Page Count: %d.\n";
	fprintf(StdHandle, OutputFormat, MiZeroedPageCount);
	
	OutputFormat = "Free Physical Page Count: %d.\n\n";
	fprintf(StdHandle, OutputFormat, MiFreePageCount);
	
	
	//////////////////////////////////////////////////////////////////////////
	//
	// 分配一块新的虚拟内存。但是没有使用 MEM_COMMIT 标志为其分配物理页。
	//
	PVOID BaseAddress = 0;
	SIZE_T RegionSize = 1;	
	Status = MmAllocateVirtualMemory(&BaseAddress, &RegionSize, MEM_RESERVE, TRUE);
	if (!EOS_SUCCESS(Status)) {
		fprintf(StdHandle, "Allocate virtual memory at 0x%X faild.\n", BaseAddress);
		goto VM_RETURN;
	}
	
	//
	// 输出新分配的内存的基址和大小
	//
	OutputFormat = "New VM's base address: 0x%X. Size: 0x%X.\n\n";
	fprintf(StdHandle, OutputFormat, BaseAddress, RegionSize);
	
	//
	// 遍历 VAD 链表，输出所有 VAD 的起始页框号，结束页框号和包含的虚拟页框数量
	//
	Index = AllocatedVpnCount = 0;
	for(pListEntry = pVadList->VadListHead.Next;
		pListEntry != &pVadList->VadListHead;
		pListEntry = pListEntry->Next) {
	
		Index++;
		pVad = CONTAINING_RECORD(pListEntry, MMVAD, VadListEntry);
		
		VpnCount = pVad->EndVpn - pVad->StartingVpn + 1;
		OutputFormat = "%d# Vad Include %d Vpn From %d to %d. (0x%X - 0x%X)\n";
		fprintf(StdHandle, OutputFormat,
			Index, VpnCount, pVad->StartingVpn, pVad->EndVpn,
			pVad->StartingVpn * PAGE_SIZE, (pVad->EndVpn + 1) * PAGE_SIZE - 1);
		
		AllocatedVpnCount += VpnCount;
	}
	
	//
	// 统计已分配的虚拟页框和未分配的虚拟页框
	//
	OutputFormat = "\nAllocated Vpn Count: %d.\n";
	fprintf(StdHandle, OutputFormat, AllocatedVpnCount);
	
	FreeVpnCount = TotalVpnCount - AllocatedVpnCount;
	OutputFormat = "Free Vpn Count: %d.\n\n";
	fprintf(StdHandle, OutputFormat, FreeVpnCount);
	
	//
	// 输出物理页的零页数量和空闲页数量
	//
	OutputFormat = "Zeroed Physical Page Count: %d.\n";
	fprintf(StdHandle, OutputFormat, MiZeroedPageCount);
	
	OutputFormat = "Free Physical Page Count: %d.\n\n";
	fprintf(StdHandle, OutputFormat, MiFreePageCount);
	
	
	//////////////////////////////////////////////////////////////////////////
	//
	// 释放刚刚分配的虚拟内存。
	//
	RegionSize = 0;		// 所释放虚拟内存的大小必须赋值为 0
	MmFreeVirtualMemory(&BaseAddress, &RegionSize, MEM_RELEASE, TRUE);
	
	//
	// 输出释放的的虚拟内存的基址和大小
	//
	OutputFormat = "Free VM's base address: 0x%X. Size: 0x%X.\n\n";
	fprintf(StdHandle, OutputFormat, BaseAddress, RegionSize);
	
	//
	// 遍历 VAD 链表，输出所有 VAD 的起始页框号，结束页框号和包含的虚拟页框数量
	//
	Index = AllocatedVpnCount = 0;
	for(pListEntry = pVadList->VadListHead.Next;
		pListEntry != &pVadList->VadListHead;
		pListEntry = pListEntry->Next) {
	
		Index++;
		pVad = CONTAINING_RECORD(pListEntry, MMVAD, VadListEntry);
		
		VpnCount = pVad->EndVpn - pVad->StartingVpn + 1;
		OutputFormat = "%d# Vad Include %d Vpn From %d to %d. (0x%X - 0x%X)\n";
		fprintf(StdHandle, OutputFormat,
			Index, VpnCount, pVad->StartingVpn, pVad->EndVpn,
			pVad->StartingVpn * PAGE_SIZE, (pVad->EndVpn + 1) * PAGE_SIZE - 1);
		
		AllocatedVpnCount += VpnCount;
	}
	
	//
	// 统计已分配的虚拟页框和未分配的虚拟页框
	//
	OutputFormat = "\nAllocated Vpn Count: %d.\n";
	fprintf(StdHandle, OutputFormat, AllocatedVpnCount);
	
	FreeVpnCount = TotalVpnCount - AllocatedVpnCount;
	OutputFormat = "Free Vpn Count: %d.\n\n";
	fprintf(StdHandle, OutputFormat, FreeVpnCount);
	
	//
	// 输出物理页的零页数量和空闲页数量
	//
	OutputFormat = "Zeroed Physical Page Count: %d.\n";
	fprintf(StdHandle, OutputFormat, MiZeroedPageCount);
	
	OutputFormat = "Free Physical Page Count: %d.\n\n";
	fprintf(StdHandle, OutputFormat, MiFreePageCount);
	
VM_RETURN:	
	KeEnableInterrupts(IntState);	// 开中断
	
	ObDerefObject(pProcCtrlBlock);
}
```

### 如果分配了物理页后，没有回收，会对 EOS 操作系统造成什么样的影响?

如果分配了物理页后，没有回收，将会使可分配自由页和零页越来越少，最终导致内存溢出，系统无法运行。

### 尝试从性能的角度分析内核函数 MiAllocateAnyPages 和 MiAllocateZeroedPages。尝试从安全性的角度分析分配零页的必要性。

系统启动时，所有空闲物理页都是未初始化的，此时零页链表为空，MiAllocateAnyPages函数可以直接从自由页链表分配，而MiAllocateZeroedPages函数会对从自由页链表中分配的每一页进行零初始化，确保所有分配页都是被零初始化的，再进行分配，因此MiAllocateZeroedPages函数效率较低。但因为MiAllocateZeroedPages函数对自由页进行了初始化，减小了出错的可能性，从而安全性较高。

### 虚拟页描述符链表中产生空隙的原因

产生空隙是由于虚拟页被释放而造成的。当一个线程或进程结束后，其资源所占用的虚拟页也就被释放了。

### MEM_RESERVE 标志和 MEM COMMIT 标志的区别

使用MEM_RESERVE标志分配虚拟页时,没有为其映射实际的物理页。使用MEM_COMMIT标志分配虚拟页时,会为其映射实际的物理页。

---

> 作者: VocabVictor  
> URL: https://cs-blog-beta.vercel.app/%E6%AF%95%E4%B8%9A%E8%AE%BE%E8%AE%A1-%E5%89%AF%E6%9C%AC-2-%E5%89%AF%E6%9C%AC/  

