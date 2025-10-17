package com.ruoyi.web.controller.classroom;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.toolkit.Wrappers;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.utils.StringUtils;
import com.ruoyi.system.domain.CameraRecords;
import com.ruoyi.system.mapper.CameraRecordsMapper;
import org.springframework.web.bind.annotation.*;

import jakarta.annotation.Resource;

/**
 * 摄像头检测记录控制器
 * 
 * @author ruoyi
 */
@RestController
@RequestMapping("/cameraRecords")
public class CameraRecordsController {
    
    @Resource
    private CameraRecordsMapper cameraRecordsMapper;

    /**
     * 获取所有记录
     */
    @GetMapping("/all")
    public AjaxResult GetAll() {
        return AjaxResult.success(cameraRecordsMapper.selectList(null));
    }

    /**
     * 根据ID获取记录
     */
    @GetMapping("/{id}")
    public AjaxResult getById(@PathVariable int id) {
        return AjaxResult.success(cameraRecordsMapper.selectById(id));
    }

    /**
     * 分页查询
     */
    @GetMapping
    public AjaxResult findPage(@RequestParam(defaultValue = "1") Integer pageNum,
                              @RequestParam(defaultValue = "10") Integer pageSize,
                              @RequestParam(defaultValue = "") String search,
                              @RequestParam(defaultValue = "") String search1,
                              @RequestParam(defaultValue = "") String search3,
                              @RequestParam(defaultValue = "") String search2) {
        LambdaQueryWrapper<CameraRecords> wrapper = Wrappers.<CameraRecords>lambdaQuery();
        wrapper.orderByDesc(CameraRecords::getStartTime);
        if (StringUtils.isNotBlank(search)) {
            wrapper.like(CameraRecords::getUsername, search);
        }
        if (StringUtils.isNotBlank(search1)) {
            wrapper.like(CameraRecords::getStartTime, search1);
        }
        if (StringUtils.isNotBlank(search2)) {
            wrapper.like(CameraRecords::getWeight, search2);
        }
        if (StringUtils.isNotBlank(search3)) {
            wrapper.like(CameraRecords::getConf, search3);
        }
        Page<CameraRecords> page = cameraRecordsMapper.selectPage(new Page<>(pageNum, pageSize), wrapper);
        return AjaxResult.success(page);
    }

    /**
     * 删除记录（支持单个和批量删除）
     */
    @DeleteMapping("/delete/{ids}")
    public AjaxResult delete(@PathVariable String ids) {
        if (ids.contains(",")) {
            // 批量删除
            String[] idArray = ids.split(",");
            for (String id : idArray) {
                cameraRecordsMapper.deleteById(Integer.parseInt(id.trim()));
            }
        } else {
            // 单个删除
            cameraRecordsMapper.deleteById(Integer.parseInt(ids));
        }
        return AjaxResult.success();
    }

    /**
     * 更新记录
     */
    @PutMapping("/updates")
    public AjaxResult updates(@RequestBody CameraRecords cameraRecords) {
        cameraRecordsMapper.updateById(cameraRecords);
        return AjaxResult.success();
    }

    /**
     * 保存记录
     */
    @PostMapping
    public AjaxResult save(@RequestBody CameraRecords cameraRecords) {
        cameraRecordsMapper.insert(cameraRecords);
        return AjaxResult.success();
    }
}

