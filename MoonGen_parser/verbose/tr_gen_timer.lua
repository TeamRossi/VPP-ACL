--- Forward packets between two ports
local lm     = require "libmoon"
local device = require "device"
local stats  = require "stats"
local log    = require "log"
local memory = require "memory"
local timer  = require "timer"
local math   = require "math"
local bit    = require "bitopt"
local ffi    = require "ffi"
local icmp   = require "proto.icmp"
local stats  = require "stats"


function configure(parser)
	parser:argument("dev", "Devices to use."):args(2):convert(tonumber)	-- args(min_number_of_args)
	parser:argument("filename", "Filename with classbench trace"):args(1)
	--parser:argument("filename", "Filename with classbench trace"):args(1):convert(io.open)	
	parser:option("-t --threads", "Number of threads per forwarding direction using RSS."):args(1):convert(tonumber):default(1)
	parser:option("-s --size", "Packet size."):default(60):convert(tonumber)
	parser:option("-r --txrate", "TX_Rate - in MBit/s."):args(1):convert(tonumber):default(0)
	return parser:parse()
end

function master(args)
	RX_TX_QUEUES = 4

	local txrate = args.txrate

	-- configure devices
	for i, dev in ipairs(args.dev) do
		args.dev[i] = device.config{
			port = dev,
			speed = txrate,
			-- leonardo: using a single queue
			txQueues = RX_TX_QUEUES,
			rxQueues = RX_TX_QUEUES,
			rssQueues = RX_TX_QUEUES
		}
	end

	--Added by Valerio
	print("Valerio parser")
	--local file="/home/valerio/filters/acl1_100_trace"
	local file=args.filename
	print("Filename: " .. file)
	local lines = lines_from(file)
	local rules_icmp = {}
	local rules_tcp = {}
	local rules_udp = {}
	--File parsing
	for k,v in pairs(lines) do
		--  print('line[' .. k .. ']', v)
		local words = {}
		local i=1
		for w in (v .. "\t"):gmatch("([^\t]*)\t") do
			table.insert(words, tonumber(w))
			i=i+1
		end
		if tonumber(words[5]) == 1 then
			table.insert(rules_icmp, words)
		elseif tonumber(words[5]) == 6 then
			table.insert(rules_tcp, words)
		else 
			table.insert(rules_udp, words)
		end
	end

--[[
	for k,v in pairs(rules_icmp) do
		io.write("line " .. k .. ": ")
		for i,j in pairs(v) do
			io.write(" " .. j)
		end
		io.write("\n")
	end
--]]
	

	local tcp_nrules = table.getn(rules_tcp)
	local udp_nrules = table.getn(rules_udp)
	local icmp_nrules = table.getn(rules_icmp)
	local tot_rules = tcp_nrules + udp_nrules + icmp_nrules 
	print("Tot_rules: " .. tot_rules)
	print("Tcp: " .. tcp_nrules .. " |Udp: " .. udp_nrules .. " |Icmp: " .. icmp_nrules)
	print("Valerio parser end")

	--Valerio end


	device.waitForLinks()


	stats.startStatsTask{devices = args.dev}

--[[
	--Valerio's stats
	local vtargs = {}
	-- print stats
	vtargs.rxDevices = {}
        vtargs.txDevices = {}
	table.insert(vtargs.txDevices, args.dev[1])
        table.insert(vtargs.rxDevices, args.dev[2])
	vtask.startStatsTask(vtargs)

	--Valerio end
]]--


	print("Pkt size: " .. args.size)	
	pkt_size = args.size

--[[
	rateq1 = math.floor(txrate * tcp_nrules/tot_rules)
	rateq2 = math.ceil(txrate * udp_nrules/tot_rules)
	rateq3 = math.ceil(txrate * icmp_nrules/tot_rules)
--]]
	rateq1 = txrate
	rateq2 = txrate
	rateq3 = txrate
	print("TX rate: " .. txrate .. " rateq1: " .. rateq1 .. " rateq2: ".. rateq2 .. " rateq3: " .. rateq3)	
--	local TxQueue0 = args.dev[1]:getTxQueue(0)
--	local TxQueue0 = args.dev[1]:getTxQueue(0):setRate(rateq1)

	args.dev[1]:getTxQueue(0):setRate(rateq1)
	args.dev[1]:getTxQueue(1):setRate(rateq2)
	args.dev[1]:getTxQueue(2):setRate(rateq3)

	-- Using a single queue
	--TX tasks
	if table.getn(rules_tcp) > 0 then
		lm.startTask("simple_forward_tcp", args.dev[1]:getTxQueue(0), rules_tcp, pkt_size)
	end
	if table.getn(rules_udp) > 0 then
		lm.startTask("simple_forward_udp", args.dev[1]:getTxQueue(1), rules_udp, pkt_size)
	end
	if table.getn(rules_icmp) > 0 then
		lm.startTask("simple_forward_icmp", args.dev[1]:getTxQueue(2), rules_icmp, pkt_size)
	end


	lm.waitForTasks()

end


function simple_forward_tcp(txQueue, rules, pkt_size)
	local framesize=pkt_size
        local counter=1
	local nrules=table.getn(rules)


	local tcpPayloadLen = framesize - 14 - 20 - 20
	local tcpPayload = ffi.new("uint8_t[?]", tcpPayloadLen)
	for i = 0, tcpPayloadLen - 1 do
		--tcpPayload[i] = bit:band(i, 0xF)
		tcpPayload[i] = bit:band(math.random(0xFF), 0xFF)
	end


	local mem = memory.createMemPool(function(buf)
		local pkt = buf:getTcpPacket()
		pkt:fill{
			pktlength=framesize,
			ethSrc = txQueue,
			ethDst = "00:25:b5:01:00:0f",
			tcpPsh = 1, 
			tcpAck = 1, 
			tcpSeqNumber = bit:band(math.random(0xFF), 0xFF),
			tcpWindow = 15
		}

		-- fill udp payload with prepared tcp payload
		ffi.copy(pkt.payload, tcpPayload, tcpPayloadLen)
	end)


	local bufs = mem:bufArray()

	local totalSent = 0
	local timer = timer:new(25)
	while (timer:running()) do
		bufs:alloc(framesize)

		for _, buf in ipairs(bufs) do
			local pkt = buf:getTcpPacket()
			local pointer = rules[counter]
			pkt.ip4:setSrc(pointer[1])
			pkt.ip4:setDst(pointer[2])
			pkt.tcp:setSrcPort(pointer[3])
			pkt.tcp:setDstPort(pointer[4])
			if counter < (nrules - 1) then counter = counter +1 
			else counter = 1 end
			--print(pointer[1] .. ", " .. pointer[2] .. ", " .. pointer[3] .. ", " .. pointer[4] )
			--buf:dump()
			--pkt.ip4:getString()
		end
		bufs:offloadTcpChecksums()
		txQueue:send(bufs)
		--totalSent = totalSent + txQueue:send(bufs)
	end

--	printf ("Total sent: %d", totalSent)

	lm.stop()

end


function simple_forward_udp(txQueue, rules, pkt_size)
	local framesize=pkt_size
        local counter=1
	local nrules=table.getn(rules)

	local udpPayloadLen = framesize - 14 - 20 - 8
	local udpPayload = ffi.new("uint8_t[?]", udpPayloadLen)
	for i = 0, udpPayloadLen - 1 do
		--udpPayload[i] = bit:band(i, 0xF)
		udpPayload[i] = bit:band(math.random(0xFF), 0xFF)
	end


	local mem = memory.createMemPool(function(buf)
		local pkt = buf:getUdpPacket()
		pkt:fill{
			pktlength=framesize,
			ethSrc = txQueue,
			ethDst = "00:25:b5:01:00:0f",
		}
		-- fill udp payload with prepared udp payload
		ffi.copy(pkt.payload, udpPayload, udpPayloadLen)

	end)


	local bufs = mem:bufArray()

	local totalSent = 0
	local timer = timer:new(25)
	while (timer:running()) do
		bufs:alloc(framesize)

		for _, buf in ipairs(bufs) do
			local pkt = buf:getUdpPacket()
			local pointer = rules[counter]
			pkt.ip4:setSrc(pointer[1])
			pkt.ip4:setDst(pointer[2])
			pkt.udp:setSrcPort(pointer[3])
			pkt.udp:setDstPort(pointer[4])
			if counter < (nrules - 1) then counter = counter +1 
			else counter = 1 end
			--buf:dump()
			--pkt.ip4:getString()
		end
		bufs:offloadUdpChecksums()
		txQueue:send(bufs)
		--totalSent = totalSent + txQueue:send(bufs)
	end

--	printf ("Total sent: %d", totalSent)

	lm.stop()

end


function simple_forward_icmp(txQueue, rules, pkt_size)
	local framesize=pkt_size
        local counter=1
	local nrules=table.getn(rules)

	local icmpBodyLen = framesize - 14 - 20 - 4
	local icmpBody = ffi.new("uint8_t[?]", icmpBodyLen)
	for i = 0, icmpBodyLen - 1 do
		--icmpBody[i] = bit:band(i, 0xF)
		icmpBody[i] = bit:band(math.random(0xFF), 0xFF)
	end


	local mem = memory.createMemPool(function(buf)
		local pkt = buf:getIcmpPacket()
		pkt:fill{
			pktlength=framesize,
			ethSrc = txQueue,
			ethDst = "00:25:b5:01:00:0f",
			pkt.icmp:setType(icmp.ECHO_REPLY.type)
		}

		-- fill udp payload with prepared tcp payload
		ffi.copy(pkt.payload, icmpBody, icmpBodyLen)
	end)


	local bufs = mem:bufArray()

	local totalSent = 0
	local timer = timer:new(25)
	while (timer:running()) do
		bufs:alloc(framesize)

		for _, buf in ipairs(bufs) do
			local pkt = buf:getIcmpPacket()
			local pointer = rules[counter]
			pkt.ip4:setSrc(pointer[1])
			pkt.ip4:setDst(pointer[2])
			pkt.icmp:calculateChecksum(pkt.ip4:getLength() - pkt.ip4:getHeaderLength() * 4)
			pkt.ip4:setChecksum(0)
			if counter < (nrules - 1) then counter = counter +1 
			else counter = 1 end
			--buf:dump()
			--pkt.ip4:getString()
		end
		bufs:offloadIPChecksums()
		--totalSent = totalSent + txQueue:send(bufs)
		txQueue:send(bufs)
	end

--	printf ("Total sent: %d", totalSent)

	lm.stop()

end




-- =========================================================

-- see if the file exists
function file_exists(file)
  local f = io.open(file, "rb")
  if f then 
	f:close() 
	print("Error with file! " .. file)
	end
  return f ~= nil
end

-- get all lines from a file, returns an empty 
-- list/table if the file does not exist
function lines_from(file)
  if not file_exists(file) then return {} end
  lines = {}
  for line in io.lines(file) do
    lines[#lines + 1] = line
  end
  return lines
end




-- =========================================================
