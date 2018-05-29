--- Replay a pcap file.

local mg      = require "moongen"
local device  = require "device"
local memory  = require "memory"
local stats   = require "stats"
local log     = require "log"
local pcap    = require "pcap"
local limiter = require "software-ratecontrol"
local vtask  = require ("valetask")
local timer  = require "timer"


function configure(parser)
	parser:argument("dev", "Device to use."):args(2):convert(tonumber)
	parser:argument("file", "File to replay."):args(1)
	parser:option("-r --rate-multiplier", "Speed up or slow down replay, 1 = use intervals from file, default = replay as fast as possible"):default(0):convert(tonumber):target("rateMultiplier")
	parser:flag("-l --loop", "Repeat pcap file.")
	local args = parser:parse()
	return args
end

function master(args)

        -- configure devices
        for i, dev in ipairs(args.dev) do
                args.dev[i] = device.config{
                        port = dev,
                }
        end

	device.waitForLinks()

	local rateLimiter
	if args.rateMultiplier > 0 then
		rateLimiter = limiter:new(dev:getTxQueue(0), "custom")
	end

--	stats.startStatsTask{txDevices = {dev}}
--      stats.startStatsTask{devices = args.dev}

        --Valerio's stats
        local vtargs = {}
        -- print stats
        vtargs.rxDevices = {}
        vtargs.txDevices = {}
        table.insert(vtargs.txDevices, args.dev[1])
        table.insert(vtargs.rxDevices, args.dev[2])
	print(vtargs)
        vtask.startStatsTask(vtargs)

	mg.startTask("replay", args.dev[1]:getTxQueue(0), args.file, args.loop, rateLimiter, args.rateMultiplier)
	mg.waitForTasks()
end

function replay(queue, file, loop, rateLimiter, multiplier)
	local mempool = memory:createMemPool(4096)
	local bufs = mempool:bufArray()
	local pcapFile = pcap:newReader(file)
	local prev = 0
	local linkSpeed = queue.dev:getLinkStatus().speed
        local timer = timer:new(25)
        while (timer:running()) do
		local n = pcapFile:read(bufs)
		if n > 0 then
			if rateLimiter ~= nil then
				if prev == 0 then
					prev = bufs.array[0].udata64
				end
				for i, buf in ipairs(bufs) do
					-- ts is in microseconds
					local ts = buf.udata64
					local delay = ts - prev
					delay = tonumber(delay * 10^3) / multiplier -- nanoseconds
					delay = delay / (8000 / linkSpeed) -- delay in bytes
					buf:setDelay(delay)
					prev = ts
				end
			end
		else
			if loop then
				pcapFile:reset()
			else
				break
			end
		end
		if rateLimiter then
			rateLimiter:sendN(bufs, n)
		else
			queue:sendN(bufs, n)
		end
	end

        mg.stop()


end

