__author__ = 'M0rdreck'
__version__ = '1.9.3'

import clr
import sys
import math
clr.AddReferenceByPartialName("UnityEngine")
clr.AddReferenceByPartialName("Pluton")
import UnityEngine
import Pluton

class Remove:
    def config(self):
        if (Plugin.IniExists("resource")):
            return Plugin.GetIni("resource")
        else:
            Plugin.CreateIni("resource")
            ini = Plugin.GetIni("resource")
            ini.AddSetting("Config", "language", "en")
            ini.AddSetting("Config", "remove", "1")
            ini.AddSetting("Config", "owner", "1")
            ini.AddSetting("Config", "destroy", "1")
            ini.AddSetting("Config", "remove_delay", "15000")
            ini.AddSetting("Config", "owner_delay", "15000")
            ini.AddSetting("Config", "destroy_delay", "15000")
            ini.Save()
            return ini

    def share(self):
        if (Plugin.IniExists("owner_share")):
            return Plugin.GetIni("owner_share")
        else:
            Plugin.CreateIni("owner_share")
            return Plugin.Getini("owner_share")

    def user(self, gid):
        if (Plugin.IniExists("owner_"+str(gid))):
            return Plugin.GetIni("owner_"+str(gid))
        else:
            return Plugin.CreateIni("owner_"+str(gid))

    def language(self):
        if (Plugin.IniExists("resource_language")):
            return Plugin.GetIni("resource_language")
        else:
            Plugin.CreateIni("resource_language")
            return Plugin.Getini("resource_language")

    def setGlobal(self, key, value):
        g = globals()
        g[key] = value

    def getGlobal(self, key):
        g = globals()
        if key in g:
            return g[key]
        else:
            return None

    def On_PlayerConnected(self, player):
        u = self.user(str(player.GameID))
        self.setGlobal("owner_" + str(player.GameID), u)

    def On_PluginInit(self):
        DataStore.Flush("destroy")
        DataStore.Flush("owner")
        # LOAD INI CONFIG
        global iniConfig
        iniConfig = self.config()
        # LOAD INI LANG
        global iniLang
        iniLang = self.language()
        # LOAD INI SHARE
        global iniShare
        iniShare = self.share()
        for p in Server.ActivePlayers:
            u = self.user(str(p.GameID))
            self.setGlobal("owner_" + str(p.GameID), u)
        for p in Server.SleepingPlayers:
            u = self.user(str(p.GameID))
            self.setGlobal("owner_" + str(p.GameID), u)
        Commands.Register("destroyConfig")\
            .setCallback(self.cmdDestroyConfig)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "description_config_list"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "usage_config_list"))
        Commands.Register("destroyConfigUpdate")\
            .setCallback(self.cmdDestroyConfigUpdate)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "description_config_update"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "usage_config_update"))
        Commands.Register("owner")\
            .setCallback(self.cmdOwner)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "description_owner"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "usage_owner"))
        Commands.Register("destroy")\
            .setCallback(self.cmdDestroy)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "description_destroy"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "usage_destroy"))
        Commands.Register("share")\
            .setCallback(self.cmdShare)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "description_share"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "usage_share"))
        Commands.Register("unshare")\
            .setCallback(self.cmdUnshare)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "description_unshare"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "usage_unshare"))
        Commands.Register("remove")\
            .setCallback(self.cmdRemove)\
                .setDescription(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "description_remove"))\
                    .setUsage(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "usage_remove"))


    def cmdDestroyConfig(self, args, player):
        if not player.Admin:
            return
        enum = iniConfig.EnumSection("Config")
        player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "config_titre_liste"))
        for key in enum:
            player.Message(str(key) + " = " + iniConfig.GetSetting("Config", key))
        player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "config_how_to"))

    def cmdDestroyConfigUpdate(self, args, player):
        if not player.Admin:
            return
        config = iniConfig.GetSetting("Config", str(args[0]))
        if(config != "" and config is not None):
            iniConfig.AddSetting("Config", str(args[0]), str(args[1]))
            player.Message(str(args[0]) + " = " + str(args[1]))
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "config_update"))
        else:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "config_not_found"))

    def cmdRemove(self, args, player):
        if not player.Admin:
            return
        if iniConfig.GetSetting("Config", "remove") == str(1):
            isdestroying = DataStore.Get("remove", player.GameID)
            if isdestroying is not None:
                DataStore.Remove("remove", player.GameID)
                player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "remove_desactivate"))
            else:
                DataStore.Add("remove", player.GameID, True)
                mydict = Plugin.CreateDict()
                mydict["gid"] = player.GameID
                Plugin.CreateParallelTimer("removerDeactivator", float(iniConfig.GetSetting("Config", "remove_delay")), mydict).Start()
                player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "remove_activate"))
        else:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "remove_server_desactivate"))

    def cmdOwner(self, args, player):
        ini = self.getGlobal("owner_" + str(player.GameID))
        if ini == "" or ini is None:
            ini = self.user(str(player.GameID))
            self.setGlobal("owner_" + str(player.GameID), ini)
        quotedargs = Util.GetQuotedArgs(args)
        if not player.Admin:
            return
        if iniConfig.GetSetting("Config", "owner") == str(1):
            isowner = DataStore.Get("owner", str(player.GameID))
            if isowner is not None:
                DataStore.Remove("owner", str(player.GameID))
                player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "owner_desactivate"))
            else:
                DataStore.Add("owner", str(player.GameID), True)
                mydict = Plugin.CreateDict()
                mydict["gid"] = player.GameID
                Plugin.CreateParallelTimer("ownerDeactivator",  float(iniConfig.GetSetting("Config", "owner_delay")), mydict).Start()
                player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "owner_activate"))
        else:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "owner_server_desactivate"))

    def cmdDestroy(self, args, player):
        ini = self.getGlobal("owner_" + str(player.GameID))
        if ini == "" or ini is None:
            ini = self.user(str(player.GameID))
            self.setGlobal("owner_" + str(player.GameID), ini)
        quotedArgs = Util.GetQuotedArgs(args)
        isdestroying = DataStore.Get("destroy", str(player.GameID))
        if iniConfig.GetSetting("Config", "destroy") == str(1):
            if isdestroying is not None:
                DataStore.Remove("destroy", str(player.GameID))
                player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "destroy_desactivate"))
            else:
                DataStore.Add("destroy", str(player.GameID), True)
                mydict = Plugin.CreateDict()
                mydict["gid"] = player.GameID
                Plugin.CreateParallelTimer("destroyDeactivator",  float(iniConfig.GetSetting("Config", "destroy_delay")), mydict).Start()
                player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "destroy_activate"))
        else:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "destroy_server_desactivate"))

    def cmdShare(self, args, player):
        quotedArgs = Util.GetQuotedArgs(args)
        if quotedArgs[0] is None:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "player_not_found"))
            return
        for p in Server.ActivePlayers:
            if(p.Name.lower() == quotedArgs[0].lower()):
                if iniShare.GetSetting(str(player.GameID), str(p.GameID)) != "" and iniShare.GetSetting(str(player.GameID), str(p.GameID)) == str(1):
                    player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "share_found") + " " + p.Name)
                    if iniShare.GetSetting(str(p.GameID), str(player.GameID)) != "" and iniShare.GetSetting(str(p.GameID), str(player.GameID)) == str(2):
                        iniShare.SetSetting(str(p.GameID), str(player.GameID), str(2))
                        iniShare.Save()
                    return
                else:
                    iniShare.SetSetting(str(p.GameID), str(player.GameID), str(2))
                    iniShare.SetSetting(str(player.GameID), str(p.GameID), str(1))
                    iniShare.Save()
                    player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "share_activate") + " " + p.Name)
                    p.Message(player.Name + " " + iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "share_with_activate"))
                    return
        player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "player_not_found"))

    def cmdUnshare(self, args, player):
        quotedArgs = Util.GetQuotedArgs(args)
        if quotedArgs[0] is None:
            player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "player_not_found"))
            return
        for p in Server.ActivePlayers:
            if(p.Name.lower() == quotedArgs[0].lower()):
                if iniShare.GetSetting(str(player.GameID), str(p.GameID)) == "" or iniShare.GetSetting(str(player.GameID), str(p.GameID)) == str(0):
                    if iniShare.GetSetting(str(p.GameID), str(player.GameID)) == "" or iniShare.GetSetting(str(p.GameID), str(player.GameID)) != str(0):
                        iniShare.SetSetting(str(p.GameID), str(player.GameID), str(0))
                        iniShare.Save()
                    player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "share_already_desactivate") + " " + p.Name)
                    return
                else:
                    iniShare.SetSetting(str(p.GameID), str(player.GameID), str(0))
                    iniShare.SetSetting(str(player.GameID), str(p.GameID), str(0))
                    iniShare.Save()
                    player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "share_deactivate") + " " + p.Name)
                    p.Message(player.Name + " " + iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "share_with_deactivate"))
                    return
        player.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "player_not_found"))

    def shareControl(self, gid, loc, locP, bb):
        enum = iniShare.EnumSection(str(gid))
        for key in enum:
            if iniShare.GetSetting(str(gid), str(key)) == str(2):
                iniu = self.getGlobal("owner_" + str(key))
                if iniu == "" or iniu is None:
                    iniu = self.user(str(gid))
                    self.setGlobal("owner_" + str(gid), iniu)
                if(iniu.GetSetting("object", loc) != "" and iniu.GetSetting("object", loc) == str(key) or iniu.GetSetting("object", locP) == str(key)):
                    Util.DestroyEntity(bb)
                    iniu.DeleteSetting("object", loc)
                    iniu.Save()
                    return

    def On_BuildingPartAttacked(self, attacked):
        bhe = attacked.Victim
        player = attacked.Attacker.ToPlayer()
        gid = player.userID
        ini = self.getGlobal("owner_" + str(gid))
        if ini == "" or ini is None:
            ini = self.user(str(gid))
            self.setGlobal("owner_" + str(gid), ini)
        if player is not None:
            loc = str(bhe.X) + str(bhe.Y) + str(bhe.Z) + attacked.Victim.buildingBlock.blockDefinition.name
            locP = str(bhe.X) + str(bhe.Y) + str(bhe.Z) + attacked.Victim.Prefab
            if Server.Players[player.userID].Admin:
                if DataStore.Get("remove", gid) is not None:
                    Util.DestroyEntity(attacked.Victim.buildingBlock)
                    for p in Server.ActivePlayers:
                        i = self.getGlobal("owner_" + str(p.GameID))
                        if i == "" or i is None:
                            i = self.user(str(p.GameID))
                            self.setGlobal("owner_" + str(p.GameID), i)
                        ownerGID = i.GetSetting("object", loc)
                        ownerGIDP = i.GetSetting("object", locP)
                        if(str(p.GameID) == str(ownerGID) or str(p.GameID) == str(ownerGIDP)):
                            ini.DeleteSetting("object", loc)
                            ini.DeleteSetting("object", locP)
                            ini.Save()
                    for p in Server.SleepingPlayers:
                        i = self.getGlobal("owner_" + str(p.GameID))
                        if i == "" or i is None:
                            i = self.user(str(player.GameID))
                            self.setGlobal("owner_" + str(player.GameID), i)
                        ownerGID = i.GetSetting("object", loc)
                        ownerGIDP = i.GetSetting("object", locP)
                        if(str(p.GameID) == str(ownerGID) or str(p.GameID) == str(ownerGIDP)):
                            ini.DeleteSetting("object", loc)
                            ini.DeleteSetting("object", locP)
                            ini.Save()
            if DataStore.Get("owner", str(gid)) is not None:
                if not Server.Players[player.userID].Admin:
                    Server.Players[player.userID].Message("not admin")
                    return
                for p in Server.ActivePlayers:
                    i = self.getGlobal("owner_" + str(p.GameID))
                    if i == "" or i is None:
                        i = self.user(str(p.GameID))
                        self.setGlobal("owner_" + str(p.GameID), i)
                    ownerGID = i.GetSetting("object", loc)
                    ownerGIDP = i.GetSetting("object", locP)
                    if(str(p.GameID) == str(ownerGID) or str(p.GameID) == str(ownerGIDP)):
                        Server.Players[player.userID].Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "owner_is") +" "+ p.Name)
                        return
                for p in Server.SleepingPlayers:
                    i = self.getGlobal("owner_" + str(p.GameID))
                    if i == "" or i is None:
                        i = self.user(str(p.GameID))
                        self.setGlobal("owner_" + str(p.GameID), i)
                    ownerGID = i.GetSetting("object", loc)
                    ownerGIDP = i.GetSetting("object", locP)
                    if(str(p.GameID) == str(ownerGID) or str(p.GameID) == str(ownerGIDP)):
                        Server.Players[player.userID].Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "owner_is") +" "+ p.Name)
                        return
                Server.Players[player.userID].Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "player_not_found"))
            elif DataStore.Get("destroy", str(gid)) is not None:
                if ini is not None and ini.GetSetting("object", loc) != "" or ini is not None and ini.GetSetting("object", locP) != "":
                    if ini.GetSetting("object", loc) == str(gid) or ini.GetSetting("object", locP) == str(gid):
                        Util.DestroyEntity(attacked.Victim.buildingBlock)
                        ini.DeleteSetting("object", loc)
                        ini.DeleteSetting("object", locP)
                        ini.Save()
                    else:
                        self.shareControl(gid, loc, locP, attacked.Victim.buildingBlock)
                else:
                    self.shareControl(gid, loc, locP, attacked.Victim.buildingBlock)

    def On_FrameDeployed(self, fde):
        builder = fde.Deployer
        bp = fde.BuildingPart
        gid = builder.GameID
        ini = self.getGlobal("owner_" + str(gid))
        if ini == "" or ini is None:
            ini = self.user(str(gid))
            self.setGlobal("owner_" + str(gid), ini)
        if builder is not None:
            loc = str(bp.X) + str(bp.Y) + str(bp.Z) + str(fde.BuildingPart.Prefab)
            if ini.GetSetting("object", loc) == "" or ini.GetSetting("object", loc) is None:
                ini.SetSetting("object", loc, str(gid))
                ini.Save()
                builder.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "building_save"))

    def On_BuildingUpdate(self, be):
        bp = be.BuildingPart
        builder = be.Builder
        gid = builder.GameID
        ini = self.getGlobal("owner_" + str(gid))
        if ini == "" or ini is None:
            ini = self.user(str(gid))
            self.setGlobal("owner_" + str(gid), ini)
        if builder is not None:
            loc = str(be.BuildingPart.X) + str(be.BuildingPart.Y) + str(be.BuildingPart.Z) + be.BlockName
            locP = str(be.BuildingPart.X) + str(be.BuildingPart.Y) + str(be.BuildingPart.Z) + bp.Prefab
            if ini.GetSetting("object", locP) == "" and ini.GetSetting("object", loc) == "" and be.BuildingPart.Health <= 0.5 or ini.GetSetting("object", locP) is None and ini.GetSetting("object", loc) is None and be.BuildingPart.Health <= 0.5 :
                ini.SetSetting("object", locP, str(gid))
                ini.Save()
                builder.Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "building_save"))
            if DataStore.Get("owner", str(gid)) is not None:
                if not Server.Players[gid].Admin:
                    Server.Players[gid].Message("not admin")
                    return
                for p in Server.ActivePlayers:
                    i = self.getGlobal("owner_" + str(p.GameID))
                    if i == "" or i is None:
                        i = self.user(str(p.GameID))
                        self.setGlobal("owner_" + str(p.GameID), i)
                    ownerGID = i.GetSetting("object", loc)
                    ownerGIDP = i.GetSetting("object", locP)
                    if(str(p.GameID) == str(ownerGID) or str(p.GameID) == str(ownerGIDP)):
                        Server.Players[gid].Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "owner_is") +" "+ p.Name)
                        return
                for p in Server.SleepingPlayers:
                    i = self.getGlobal("owner_" + str(p.GameID))
                    if i == "" or i is None:
                        i = self.user(str(p.GameID))
                        self.setGlobal("owner_" + str(p.GameID), i)
                    ownerGID = i.GetSetting("object", loc)
                    ownerGIDP = i.GetSetting("object", locP)
                    if(str(p.GameID) == str(ownerGID) or str(p.GameID) == str(ownerGIDP)):
                        Server.Players[gid].Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "owner_is") +" "+ p.Name)
                        return
                Server.Players[builder.userID].Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "player_not_found"))
	# xCorrosionx function
    def destroyDeactivatorCallback(self, timer):
        mydict = timer.Args
        gid = mydict["gid"]
        Server.Players[gid].Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "destroy_desactivate"))
        DataStore.Remove("destroy", str(gid))
        timer.Kill()
    def ownerDeactivatorCallback(self, timer):
        mydict = timer.Args
        gid = mydict["gid"]
        Server.Players[gid].Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "owner_desactivate"))
        DataStore.Remove("owner", str(gid))
        timer.Kill()
    def removerDeactivatorCallback(self, timer):
        mydict = timer.Args
        gid = mydict["gid"]
        Server.Players[gid].Message(iniLang.GetSetting(iniConfig.GetSetting("Config", "language"), "remove_desactivate"))
        DataStore.Remove("remove", gid)
        timer.Kill()
